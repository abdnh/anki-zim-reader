import os

from aqt import qtmajor
from aqt.main import AnkiQt
from aqt.qt import QDialog, QIcon, QKeySequence

from .. import consts, dictionaries, popup
from . import qconnect

if qtmajor <= 5:
    from ..forms.settings_qt5 import Ui_Dialog
else:
    from ..forms.settings_qt6 import Ui_Dialog  # type: ignore


class SettingsDialog(QDialog):
    def __init__(
        self,
        mw: AnkiQt,
    ):
        super().__init__(mw)
        self.form = Ui_Dialog()
        self.form.setupUi(self)
        self.mw = mw
        self.config = mw.addonManager.getConfig(__name__)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle(f"{consts.ADDON_NAME} - Settings")
        icon = QIcon(os.path.join(consts.ICONS_DIR, "logo.svg"))
        self.setWindowIcon(icon)
        self.form.icon.setPixmap(icon.pixmap(314, 314))
        qconnect(self.form.saveButton.clicked, self.on_save)
        self.form.saveButton.setShortcut(QKeySequence("Ctrl+Return"))
        dictionary_names = [p.name for p in dictionaries.get_files()]
        self.form.popupDictionaryComboBox.addItems(dictionary_names)
        configured_dictionary = self.config["popup_dictionary"]
        try:
            idx = dictionary_names.index(configured_dictionary)
        except ValueError:
            idx = 0
        self.form.popupDictionaryComboBox.setCurrentIndex(idx)
        parser_names = [parser.name for parser in dictionaries.PARSER_CLASSES]
        self.form.parserComboBox.addItems(parser_names)
        configured_parser = self.config["popup_parser"]
        try:
            idx = parser_names.index(configured_parser)
        except ValueError:
            idx = 0
        self.form.parserComboBox.setCurrentIndex(idx)
        self.form.popupShortcut.setKeySequence(
            QKeySequence(self.config["popup_shortcut"])
        )
        self.form.popupWidthSpinBox.setValue(int(self.config["popup_width"]))
        self.form.popupHeightSpinBox.setValue(int(self.config["popup_height"]))

        # TODO: make other shortcuts configurable from here too

    def on_save(self) -> None:
        popup_dictionary = self.form.popupDictionaryComboBox.currentText()
        popup_parser = self.form.parserComboBox.currentText()
        popup_shortcut = self.form.popupShortcut.keySequence().toString()
        popup_width = self.form.popupWidthSpinBox.value()
        popup_height = self.form.popupHeightSpinBox.value()
        self.config["popup_dictionary"] = popup_dictionary
        self.config["popup_parser"] = popup_parser
        self.config["popup_shortcut"] = popup_shortcut
        self.config["popup_width"] = popup_width
        self.config["popup_height"] = popup_height

        self.mw.addonManager.writeConfig(__name__, self.config)
        popup.restart_server()
        popup.reset_shortcut()
        self.accept()
