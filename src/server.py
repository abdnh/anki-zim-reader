from __future__ import annotations

import threading
from http import HTTPStatus

import flask
from flask import Flask, Response
from waitress.server import create_server as create_waitress_server

from .dictionaries import DefaultParser, Parser, ZIMDict


class ZIMServer(threading.Thread):

    _ready = threading.Event()
    daemon = True

    def __init__(self, app: Flask, dictionary: str, parser: Parser) -> None:
        super().__init__()
        self.app = app
        self.is_shutdown = False
        self.dictionary = ZIMDict(dictionary, parser)

    def run(self) -> None:
        try:
            self.server = create_waitress_server(
                self.app,
                host="127.0.0.1",
                # port="8000",
                port="0",
                clear_untrusted_proxy_headers=True,
                threads=1,
            )
            self._ready.set()
            self.server.run()

        except Exception:
            if not self.is_shutdown:
                raise

    # Copied from mediasrv.py in Anki
    def shutdown(self) -> None:
        self.is_shutdown = True
        sockets = list(self.server._map.values())  # type: ignore
        for socket in sockets:
            socket.handle_close()
        # https://github.com/Pylons/webtest/blob/4b8a3ebf984185ff4fefb31b4d0cf82682e1fcf7/webtest/http.py#L93-L104
        self.server.task_dispatcher.shutdown()

    @property
    def port(self) -> int:
        self._ready.wait()
        return int(self.server.effective_port)  # type: ignore

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}/"


def create_server(
    dictionary: str, parser: Parser = DefaultParser(), follow_redirects: bool = False
) -> ZIMServer:
    app = Flask(__name__)

    zim_server = ZIMServer(app, dictionary, parser)

    @app.route("/")
    def index() -> Response:
        item = zim_server.dictionary.client.main_page()
        response = flask.make_response(item.content, HTTPStatus.OK)
        response.headers["Content-Type"] = item.mimetype
        return response

    @app.route("/<path:path>")
    def handle_request(path: str) -> Response:
        if follow_redirects:
            try:
                path = parser.follow_redirects(path, zim_server.dictionary)
            except:
                pass
        item = zim_server.dictionary.get_item(path)
        if not item:
            *_, word = path.rsplit("/", maxsplit=1)
            item = zim_server.dictionary.client.first_result(word)
        if item:
            response = flask.make_response(item.content, HTTPStatus.OK)
            response.headers["Content-Type"] = item.mimetype
            return response
        return flask.make_response(f"{path} not found", HTTPStatus.NOT_FOUND)

    return zim_server


if __name__ == "__main__":
    server = create_server("wiktionary_el_all_maxi_2022-07")
    server.start()
    server.join()
