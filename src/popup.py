from __future__ import annotations

import json
from typing import Any

from aqt import mw
from aqt.browser.previewer import Previewer
from aqt.clayout import CardLayout
from aqt.gui_hooks import webview_did_receive_js_message, webview_will_set_content
from aqt.qt import QKeySequence, QShortcut, Qt
from aqt.reviewer import Reviewer
from aqt.webview import AnkiWebView, WebContent

from . import server
from .dictionaries import PARSER_CLASSES
from .errors import ZIMReaderException

zim_server: server.ZIMServer | None = None
shortcut: QShortcut | None = None


def append_webcontent(webcontent: WebContent, context: Any) -> None:

    if isinstance(context, (Reviewer, Previewer, CardLayout)):
        base_path = f"/_addons/{mw.addonManager.addonFromModule(__name__)}/web"

        webcontent.js.append(f"{base_path}/vendor/popper.min.js")
        webcontent.js.append(f"{base_path}/vendor/tippy.umd.min.js")
        webcontent.js.append(f"{base_path}/popup.js")

        webcontent.css.append(f"{base_path}/vendor/tippy.css")
        webcontent.css.append(f"{base_path}/vendor/scale-extreme.css")
        webcontent.css.append(f"{base_path}/vendor/light.css")
        webcontent.css.append(f"{base_path}/popup.css")


def get_webview_for_context(context: Any) -> AnkiWebView:
    if isinstance(context, Previewer):
        web = context._web  # pylint: disable=protected-access
    elif isinstance(context, CardLayout):
        web = context.preview_web
    else:
        web = context.web
    return web


def handle_popup_request(
    handled: tuple[bool, Any], message: str, context: Any
) -> tuple[bool, Any]:
    parts = message.split(":")
    cmd = parts[0]
    if cmd != "zim_server" or len(parts) == 1:
        return handled
    subcmd, word = parts[1:3]
    if subcmd == "popup":
        config = mw.addonManager.getConfig(__name__)
        width = config["popup_width"]
        height = config["popup_height"]
        contents = f"<iframe src='{zim_server.url}{word}' width='{width}' height='{height}' style='display: block;'></iframe>"
        contents = json.dumps(contents)
        web = get_webview_for_context(context)
        web.eval(
            f"globalThis.tippyInstance.setContent({contents}); globalThis.tippyInstance.setProps({{maxWidth: {width}}});"
        )
    return (True, None)


def show_tooltip() -> None:
    if not zim_server:
        return
    window = mw.app.activeWindow()
    # FIXME: not actually working in the card layouts screen
    if isinstance(window, CardLayout):
        web = window.preview_web
    elif isinstance(window, Previewer):
        web = window._web
    elif mw.state == "review":
        web = mw.reviewer.web
    else:
        return
    web.eval("showTooltipForSelection();")


def restart_server() -> None:
    global zim_server
    if zim_server:
        zim_server.shutdown()
    config = mw.addonManager.getConfig(__name__)
    dictionary = config["popup_dictionary"]
    parser_name = config["popup_parser"].lower()
    parser_names = [parser.name.lower() for parser in PARSER_CLASSES]
    try:
        parser_idx = parser_names.index(parser_name)
    except ValueError:
        parser_idx = 0
    parser = PARSER_CLASSES[parser_idx]()
    try:
        zim_server = server.create_server(dictionary, parser)
    except ZIMReaderException:
        return
    zim_server.start()


def reset_shortcut() -> None:
    config = mw.addonManager.getConfig(__name__)
    global shortcut
    if shortcut:
        shortcut.deleteLater()
    shortcut = QShortcut(  # type: ignore
        QKeySequence(config["popup_shortcut"]),
        mw,
        activated=show_tooltip,
        context=Qt.ShortcutContext.ApplicationShortcut,
    )


def init() -> None:
    restart_server()
    mw.addonManager.setWebExports(__name__, r"web(vendor)*/.*\.(js|css)")
    webview_will_set_content.append(append_webcontent)
    webview_did_receive_js_message.append(handle_popup_request)
    reset_shortcut()
