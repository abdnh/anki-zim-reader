from __future__ import annotations

import os
import time

from aqt import qtmajor
from aqt.main import AnkiQt
from aqt.qt import QDialog, QIcon, QShortcut, QSize, Qt, QUrl, QVBoxLayout, QWidget
from aqt.webview import AnkiWebView

from .. import consts, dictionaries
from ..server import ZIMServer, create_server
from . import qconnect

if qtmajor <= 5:
    from ..forms.browser_qt5 import Ui_Dialog
else:
    from ..forms.browser_qt6 import Ui_Dialog  # type: ignore


class BrowserDialog(QDialog):
    def __init__(
        self,
        mw: AnkiQt,
    ):
        super().__init__(mw, Qt.WindowType.Window)
        self.form = Ui_Dialog()
        self.form.setupUi(self)
        self.mw = mw
        self.config = mw.addonManager.getConfig(__name__)
        self.server: ZIMServer | None = None
        self.files = [p.name for p in dictionaries.get_files()]
        self.parsers = [parser.name for parser in dictionaries.PARSER_CLASSES]
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle(f"{consts.ADDON_NAME} - Browser")
        icon = QIcon(os.path.join(consts.ICONS_DIR, "logo.svg"))
        self.setWindowIcon(icon)

        qconnect(self.form.back.clicked, lambda: self.webview.page().history().back())
        qconnect(
            self.form.forward.clicked, lambda: self.webview.page().history().forward()
        )

        # Wrap webview in a widget to be able to add a border
        widget = QWidget(self)
        widget.setLayout(QVBoxLayout())
        widget.setStyleSheet("border: 1px solid grey;")
        self.webview = webview = AnkiWebView(self, "ZIM Reader Browser")
        qconnect(webview.urlChanged, self.on_url_changed)
        widget.layout().addWidget(webview)
        webview.set_open_links_externally(False)
        self.form.gridLayout.addWidget(widget, 1, 0, 10, 3)

        qconnect(self.finished, self.on_finished)
        qconnect(
            QShortcut("Ctrl+F", self).activated,
            self.form.search_edit.grabKeyboard,
        )
        qconnect(self.form.search_button.clicked, self.on_search)

        self.form.file.addItems(self.files)
        configured_dictionary = self.config["popup_dictionary"]
        try:
            idx = self.files.index(configured_dictionary)
        except ValueError:
            idx = 0
        qconnect(self.form.file.currentIndexChanged, self.on_file_changed)
        self.form.file.setCurrentIndex(idx)

        self.form.parser.addItems(self.parsers)
        configured_parser = self.config["popup_parser"]
        try:
            idx = self.parsers.index(configured_parser)
        except ValueError:
            idx = 0
        qconnect(self.form.parser.currentIndexChanged, self.on_parser_changed)
        self.form.parser.setCurrentIndex(idx)

    def on_file_changed(self, index: int) -> None:
        if self.server:
            self.server.shutdown()
        parser = dictionaries.PARSER_CLASSES[self.form.parser.currentIndex()]()
        print(self.files[index], parser)
        self.server = create_server(
            self.files[index], parser, self.form.follow_redirects.isChecked()
        )
        self.server.start()
        # Wait for server to start before accessing url
        # FIXME: this should not be necessary as .url will block until the server is initialized
        # but I'm getting an AttributeError here nevertheless for some weird reason
        time.sleep(0.01)
        self.webview.page().history().clear()
        self.webview.load_url(QUrl(self.server.url))
        self.form.address_bar.setText(self.server.url)

    def on_parser_changed(self, index: int) -> None:
        if not self.server:
            return
        parser = dictionaries.PARSER_CLASSES[self.form.parser.currentIndex()]()
        self.server.dictionary.parser = parser

    def on_search(self) -> None:
        search = self.form.search_edit.text()
        url = self.server.url + search
        self.webview.load_url(QUrl(url))
        self.form.address_bar.setText(url)

    def on_url_changed(self, url: QUrl) -> None:
        if self.webview.page().history().canGoBack():
            back_icon = "back.svg"
        else:
            back_icon = "back-disabled.svg"
        if self.webview.page().history().canGoForward():
            forward_icon = "forward.svg"
        else:
            forward_icon = "forward-disabled.svg"
        self.form.back.setIcon(QIcon(str(consts.ICONS_DIR / back_icon)))
        self.form.forward.setIcon(QIcon(str(consts.ICONS_DIR / forward_icon)))
        self.form.address_bar.setText(url.toString())

    def on_finished(self) -> None:
        if self.server:
            self.server.shutdown()
