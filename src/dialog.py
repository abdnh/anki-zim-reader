import os
from typing import Any, Callable, List, Optional, Tuple

from anki.notes import Note
from aqt import qtmajor
from aqt.main import AnkiQt
from aqt.operations import QueryOp
from aqt.qt import QDialog, QPixmap, QWidget, qconnect
from aqt.utils import showWarning

from . import consts
from .dictionaries import (
    DictEntry,
    DictException,
    Dictionary,
    Parser,
    dictionary_classes,
)

if qtmajor > 5:
    from .forms.form_qt6 import Ui_Dialog
else:
    from .forms.form_qt5 import Ui_Dialog  # type: ignore


PROGRESS_LABEL = "Updated {count} out of {total} note(s)"


class WiktionaryFetcherDialog(QDialog):
    def __init__(
        self,
        mw: AnkiQt,
        parent: QWidget,
        notes: List[Note],
    ):
        super().__init__(parent)
        self.form = Ui_Dialog()
        self.form.setupUi(self)
        self.mw = mw
        self.notes = notes
        self.combos = [
            self.form.wordFieldComboBox,
            self.form.definitionFieldComboBox,
            self.form.exampleFieldComboBox,
            self.form.genderFieldComboBox,
            self.form.POSFieldComboBox,
        ]
        self.setWindowTitle(consts.ADDON_NAME)
        self.form.icon.setPixmap(
            QPixmap(os.path.join(consts.ICONS_DIR, "enwiktionary-1.5x.png"))
        )
        self.form.providerComboBox.addItems(
            [dictionary.name for dictionary in dictionary_classes]
        )
        self.on_provider_changed(0)
        qconnect(
            self.form.providerComboBox.currentIndexChanged, self.on_provider_changed
        )

        self.dictionary: Optional[Dictionary] = None
        self.parser: Optional[Parser] = None
        qconnect(self.form.addButton.clicked, self.on_add)

    def on_provider_changed(self, index: int) -> None:
        self.form.dictionaryComboBox.clear()
        provider_path = (
            consts.USER_FILES
            / dictionary_classes[self.form.providerComboBox.currentIndex()].name
        )
        provider_path.mkdir(exist_ok=True)
        dictionary_names = [
            path.name for path in provider_path.iterdir() if path.is_dir()
        ]
        self.form.dictionaryComboBox.addItems(dictionary_names)
        parser_names = [
            parser.name
            for parser in dictionary_classes[
                self.form.providerComboBox.currentIndex()
            ].parsers
        ]
        self.form.parserComboBox.clear()
        self.form.parserComboBox.addItems(parser_names)

    def exec(self) -> int:
        if self._fill_fields():
            return super().exec()
        return QDialog.DialogCode.Rejected  # pylint: disable=no-member

    def _fill_fields(self) -> int:
        mids = set(note.mid for note in self.notes)
        if len(mids) > 1:
            showWarning(
                "Please select notes from only one notetype.",
                parent=self,
                title=consts.ADDON_NAME,
            )
            return 0
        self.field_names = ["None"] + self.notes[0].keys()
        for i, combo in enumerate(self.combos):
            combo.addItems(self.field_names)
            selected = 0
            if len(self.field_names) - 1 > i:
                selected = i + 1
            combo.setCurrentIndex(selected)
            qconnect(
                combo.currentIndexChanged,
                lambda field_index, combo_index=i: self.on_selected_field_changed(
                    combo_index, field_index
                ),
            )
        return 1

    def on_selected_field_changed(self, combo_index: int, field_index: int) -> None:
        if field_index == 0:
            return
        for i, combo in enumerate(self.combos):
            if i != combo_index and combo.currentIndex() == field_index:
                combo.setCurrentIndex(0)

    def on_add(self) -> None:
        if self.form.wordFieldComboBox.currentIndex() == 0:
            showWarning("No word field selected.", parent=self, title=consts.ADDON_NAME)
            return
        if self.form.dictionaryComboBox.currentIndex() == -1:
            showWarning(
                "No dictionary is available. Please use <b>Tools > Wiktionary > Import a dictionary</b>.",
                textFormat="rich",
            )
            return
        dictionary = self.form.dictionaryComboBox.currentText()
        dictionary_class = dictionary_classes[self.form.providerComboBox.currentIndex()]
        dictionary_path = consts.USER_FILES / dictionary_class.name / dictionary
        self.dictionary = dictionary_class(dictionary_path)
        self.parser = self.dictionary.parsers[self.form.parserComboBox.currentIndex()]()
        word_field = self.form.wordFieldComboBox.currentText()
        definition_field_i = self.form.definitionFieldComboBox.currentIndex()
        example_field_i = self.form.exampleFieldComboBox.currentIndex()
        gender_field_i = self.form.genderFieldComboBox.currentIndex()
        pos_field_i = self.form.POSFieldComboBox.currentIndex()
        field_tuples = (
            (definition_field_i, self._get_definitions),
            (example_field_i, self._get_examples),
            (gender_field_i, self._get_gender),
            (pos_field_i, self._get_part_of_speech),
        )

        def on_success(ret: Any) -> None:
            self.accept()

        def on_failure(exc: Exception) -> None:
            self.mw.progress.finish()
            # showWarning(str(exc), parent=self, title=consts.ADDON_NAME)
            self.accept()
            raise exc

        op = QueryOp(
            parent=self,
            op=lambda col: self._fill_notes(
                word_field,
                field_tuples,
            ),
            success=on_success,
        )
        op.failure(on_failure)
        op.run_in_background()
        self.mw.progress.start(
            max=len(self.notes),
            label=PROGRESS_LABEL.format(count=0, total=len(self.notes)),
            parent=self,
            immediate=True,
        )
        self.mw.progress.set_title(consts.ADDON_NAME)

    def _fill_notes(
        self,
        word_field: str,
        field_tuples: Tuple[Tuple[int, Callable[[DictEntry], str]], ...],
    ) -> None:
        want_cancel = False
        self.errors = []
        self.updated_notes: List[Note] = []

        def on_progress() -> None:
            nonlocal want_cancel
            want_cancel = self.mw.progress.want_cancel()
            self.mw.progress.update(
                label=PROGRESS_LABEL.format(
                    count=len(self.updated_notes), total=len(self.notes)
                ),
                value=len(self.updated_notes),
                max=len(self.notes),
            )

        for i, note in enumerate(self.notes):
            word = note[word_field]
            need_updating = False
            try:
                dict_entry = self.dictionary.lookup(word, self.parser)
                if not dict_entry:
                    self.errors.append(f'"{word}" was not found in the dictionary.')
                    continue
                for field_tuple in field_tuples:
                    if not field_tuple[0]:
                        continue
                    contents = field_tuple[1](dict_entry)
                    note[self.field_names[field_tuple[0]]] = contents
                    need_updating = True
            except DictException as exc:
                self.errors.append(str(exc))
            finally:
                if need_updating:
                    self.updated_notes.append(note)
                if i % 50 == 0:
                    self.mw.taskman.run_on_main(on_progress)
            if want_cancel:
                break
        self.mw.taskman.run_on_main(self.mw.progress.finish)

    def _get_definitions(self, entry: DictEntry) -> str:
        field_contents = []
        for i, definition in enumerate(entry.definitions):
            field_contents.append(f"{i+1}. {definition}")
        return "<br>".join(field_contents)

    def _get_examples(self, entry: DictEntry) -> str:
        field_contents = []
        for example in entry.examples:
            field_contents.append(example)
        return "<br>".join(field_contents)

    def _get_gender(self, entry: DictEntry) -> str:
        return entry.gender

    def _get_part_of_speech(self, entry: DictEntry) -> str:
        return entry.pos
