import os
import time
from typing import Any, Callable, List, Tuple

try:
    from anki.utils import strip_html
except ImportError:
    from anki.utils import stripHTML as strip_html

from anki.notes import Note
from aqt import qtmajor
from aqt.main import AnkiQt
from aqt.operations import QueryOp
from aqt.qt import QDialog, QIcon, QKeySequence, QWidget
from aqt.utils import showWarning

from .. import consts
from ..dictionaries import PARSER_CLASSES, DictEntry, get_files
from ..dictionaries.dictionary import ZIMDict
from ..errors import ZIMReaderException
from . import qconnect

if qtmajor <= 5:
    from ..forms.main_qt5 import Ui_Dialog
else:
    from ..forms.main_qt6 import Ui_Dialog  # type: ignore


PROGRESS_LABEL = "Updated {count} out of {total} note(s)"


class ZIMFetcherDialog(QDialog):
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
        self.config = mw.addonManager.getConfig(__name__)
        self.notes = notes
        self.combos = [
            self.form.wordFieldComboBox,
            self.form.definitionFieldComboBox,
            self.form.exampleFieldComboBox,
            self.form.genderFieldComboBox,
            self.form.POSFieldComboBox,
            self.form.inflectionFieldComboBox,
            self.form.translationFieldComboBox,
            self.form.imageFieldComboBox,
        ]
        self.setWindowTitle(consts.ADDON_NAME)
        icon = QIcon(os.path.join(consts.ICONS_DIR, "logo.svg"))
        self.setWindowIcon(icon)
        self.form.icon.setPixmap(icon.pixmap(314, 314))
        self.form.fileComboBox.addItems([file.name for file in get_files()])
        self.form.parserComboBox.addItems([parser.name for parser in PARSER_CLASSES])
        qconnect(self.form.addButton.clicked, self.on_add)
        self.form.addButton.setShortcut(QKeySequence("Ctrl+Return"))
        qconnect(self.finished, self.on_finished)

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
        self.set_last_used_settings()
        return 1

    CONFIG_MODEL_FIELDS = (
        "word_field",
        "definition_field",
        "example_field",
        "gender_field",
        "part_of_speech_field",
        "inflection_field",
        "translation_field",
        "image_field",
    )

    def set_last_used_settings(self) -> None:
        file = self.config["file_field"].lower()
        for i in range(self.form.fileComboBox.count()):
            text = self.form.fileComboBox.itemText(i)
            if text.lower() == file:
                self.form.fileComboBox.setCurrentIndex(i)
                break
        parser = self.config["parser_field"].lower()
        for i in range(self.form.parserComboBox.count()):
            text = self.form.parserComboBox.itemText(i)
            if text.lower() == parser:
                self.form.parserComboBox.setCurrentIndex(i)
                break
        for i, field_opt in enumerate(self.CONFIG_MODEL_FIELDS):
            field_name = self.config[field_opt].lower()
            combo = self.combos[i]
            for i in range(combo.count()):
                text = combo.itemText(i)
                if text.lower() == field_name:
                    combo.setCurrentIndex(i)
                    break
        self.form.skipNonEmptyCheckBox.setChecked(self.config["skip_non_empty"])

    def save_settings(self) -> None:
        self.config["file_field"] = self.form.fileComboBox.currentText()
        self.config["parser_field"] = self.form.parserComboBox.currentText()
        for i, field_opt in enumerate(self.CONFIG_MODEL_FIELDS):
            self.config[field_opt] = self.combos[i].currentText()
        self.config["skip_non_empty"] = self.form.skipNonEmptyCheckBox.isChecked()
        self.mw.addonManager.writeConfig(__name__, self.config)

    def on_finished(self, result: int) -> None:
        self.save_settings()

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
        if self.form.fileComboBox.currentIndex() == -1:
            showWarning(
                f"No dictionary is available. Please use <b>Tools > {consts.ADDON_NAME} > Import a file</b>.",
                textFormat="rich",
            )
            return
        parser = PARSER_CLASSES[self.form.parserComboBox.currentIndex()](self.mw.col)
        self.dictionary = ZIMDict.from_basedir(
            self.form.fileComboBox.currentText(), parser
        )
        skip_non_empty = self.form.skipNonEmptyCheckBox.isChecked()
        word_field = self.form.wordFieldComboBox.currentText()
        definition_field_i = self.form.definitionFieldComboBox.currentIndex()
        example_field_i = self.form.exampleFieldComboBox.currentIndex()
        gender_field_i = self.form.genderFieldComboBox.currentIndex()
        pos_field_i = self.form.POSFieldComboBox.currentIndex()
        inflection_field_i = self.form.inflectionFieldComboBox.currentIndex()
        translation_field_i = self.form.translationFieldComboBox.currentIndex()
        image_field_i = self.form.imageFieldComboBox.currentIndex()

        field_tuples = (
            (definition_field_i, self._get_definitions),
            (example_field_i, self._get_examples),
            (gender_field_i, self._get_gender),
            (pos_field_i, self._get_part_of_speech),
            (inflection_field_i, self._get_inflections),
            (translation_field_i, self._get_translations),
            (image_field_i, self._get_images),
        )

        def on_success(ret: Any) -> None:
            self.accept()

        def on_failure(exc: Exception) -> None:
            self.mw.progress.finish()
            self.accept()
            raise exc

        op = QueryOp(
            parent=self,
            op=lambda col: self._fill_notes(
                word_field,
                field_tuples,
                skip_non_empty,
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
        skip_non_empty: bool,
    ) -> None:
        want_cancel = False
        last_progress = 0.0
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
            word = strip_html(note[word_field])
            need_updating = False
            try:
                if not word:
                    continue
                dict_entry = self.dictionary.lookup(word)
                if not dict_entry:
                    self.errors.append(f'"{word}" was not found in the dictionary.')
                    continue
                for field_tuple in field_tuples:
                    if not field_tuple[0]:
                        continue
                    contents = field_tuple[1](dict_entry)
                    if not (
                        skip_non_empty
                        and note[self.field_names[field_tuple[0]]].strip()
                    ):
                        note[self.field_names[field_tuple[0]]] = contents
                        need_updating = True
            except ZIMReaderException as exc:
                self.errors.append(str(exc))
            finally:
                if need_updating:
                    self.updated_notes.append(note)
                if time.time() - last_progress >= 0.01:
                    self.mw.taskman.run_on_main(on_progress)
                    last_progress = time.time()
            if want_cancel:
                break
        self.mw.taskman.run_on_main(self.mw.progress.finish)

    def _get_definitions(self, entry: DictEntry) -> str:
        if not entry.definitions:
            return ""
        if len(entry.definitions) == 1:
            return entry.definitions[0]
        formatted = "<ul>"
        for definition in entry.definitions:
            formatted += f"<li>{definition}</li>"
        formatted += "</ul>"
        return formatted

    def _get_examples(self, entry: DictEntry) -> str:
        if not entry.examples:
            return ""
        if len(entry.examples) == 1:
            return entry.examples[0]
        formatted = "<ul>"
        for example in entry.examples:
            formatted += f"<li>{example}</li>"
        formatted += "</ul>"
        return formatted

    def _get_gender(self, entry: DictEntry) -> str:
        return entry.gender

    def _get_part_of_speech(self, entry: DictEntry) -> str:
        return entry.pos

    def _get_inflections(self, entry: DictEntry) -> str:
        return entry.inflections

    def _get_translations(self, entry: DictEntry) -> str:
        return entry.translations

    def _get_images(self, entry: DictEntry) -> str:
        return entry.images
