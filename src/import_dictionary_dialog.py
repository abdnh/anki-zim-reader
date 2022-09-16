import os
from concurrent.futures import Future
from typing import List

from aqt import qtmajor
from aqt.main import AnkiQt
from aqt.qt import QDialog, qconnect
from aqt.utils import getFile, openLink, showWarning, tooltip

from . import consts
from .dictionaries import ZIMDict

if qtmajor > 5:
    from .forms.import_dictionary_qt6 import Ui_Dialog
else:
    from .forms.import_dictionary_qt5 import Ui_Dialog  # type: ignore


class ImportDictionaryDialog(QDialog):
    def __init__(
        self,
        mw: AnkiQt,
    ):
        super().__init__(mw)
        self.form = Ui_Dialog()
        self.form.setupUi(self)
        self.mw = mw
        self.errors: List[str] = []
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle(f"{consts.ADDON_NAME} - Import a file")
        qconnect(
            self.form.chooseFileButton.clicked,
            self.on_choose_file,
        )
        qconnect(self.form.addButton.clicked, self.on_add)
        qconnect(
            self.form.description.linkActivated,
            lambda link: openLink(link),  # pylint: disable=unnecessary-lambda
        )
        self.form.description.setText(
            """Only a limited number of <a href="https://en.wikipedia.org/wiki/ZIM_(file_format)">ZIM</a> \
files listed at <a href="https://wiki.kiwix.org/wiki/Content_in_all_languages">this page</a> are supported currently."""
        )

    def on_choose_file(self) -> None:
        filename = getFile(
            self,
            title=consts.ADDON_NAME,
            cb=None,
            filter="*.zim",
            key=consts.ADDON_NAME,
        )
        if not filename:
            return
        filename = str(filename)
        self.form.filenameLabel.setText(filename)
        name, _ = os.path.splitext(os.path.basename(filename))
        self.form.dictionaryNameLineEdit.setText(name)

    def on_add(self) -> None:
        def on_done(future: Future) -> None:
            self.mw.progress.finish()
            try:
                future.result()
            except Exception as exc:
                showWarning(str(exc), parent=self, title=consts.ADDON_NAME)
                return
            tooltip("Successfully imported dictionary", parent=self.mw)
            self.accept()

        filename = self.form.filenameLabel.text()
        name = self.form.dictionaryNameLineEdit.text().strip()
        if not name or not filename:
            showWarning("Filename and dictionary name fields cannot be empty")
            return
        self.mw.progress.start(label="Starting importing...", parent=self)
        self.mw.progress.set_title(f"{consts.ADDON_NAME} - Importing a dictionary")
        output_folder = consts.USER_FILES / name
        self.mw.taskman.run_in_background(
            lambda: ZIMDict.build_dict(filename, output_folder),
            on_done=on_done,
        )
