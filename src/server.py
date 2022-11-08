from __future__ import annotations

import os
import threading
from http import HTTPStatus
from pathlib import Path

import flask
from flask import Flask, Response
from waitress.server import create_server as create_waitress_server

from .consts import USER_FILES
from .dictionaries import DefaultParser, Parser, ZIMDict


class ZIMServer(threading.Thread):

    _ready = threading.Event()
    daemon = True

    def __init__(self, app: Flask):
        super().__init__()
        self.app = app
        self.is_shutdown = False
        self.dictionary: ZIMDict | None = None

    @classmethod
    def from_path(
        cls,
        app: Flask,
        path: Path,
        parser: Parser = DefaultParser(),
    ) -> ZIMServer:
        self = ZIMServer(app)
        self.dictionary = ZIMDict(path, parser)
        return self

    @classmethod
    def from_basedir(
        cls,
        app: Flask,
        name: str,
        parser: Parser,
        base_dir: Path | str = USER_FILES,
    ) -> ZIMServer:
        self = ZIMServer(app)
        self.dictionary = ZIMDict.from_basedir(name, parser, base_dir)
        return self

    def run(self) -> None:
        try:
            port = int(os.getenv("ZIM_SERVER_PORT", "0"))
            self.server = create_waitress_server(
                self.app,
                host="127.0.0.1",
                port=port,
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


def _connect_server(server: ZIMServer, follow_redirects: bool = False) -> None:
    @server.app.route("/")
    def index() -> Response:
        item = server.dictionary.client.main_page()
        response = flask.make_response(item.content, HTTPStatus.OK)
        response.headers["Content-Type"] = item.mimetype
        return response

    @server.app.route("/<path:path>")
    def handle_request(path: str) -> Response:
        if follow_redirects:
            try:
                path = server.dictionary.parser.follow_redirects(
                    path, server.dictionary
                )
            except:
                pass
        item = server.dictionary.get_item(path)
        if not item:
            *_, word = path.rsplit("/", maxsplit=1)
            item = server.dictionary.client.first_result(word)
        if item:
            response = flask.make_response(item.content, HTTPStatus.OK)
            response.headers["Content-Type"] = item.mimetype
            return response
        return flask.make_response(f"{path} not found", HTTPStatus.NOT_FOUND)


def create_server_for_path(
    path: Path, parser: Parser = DefaultParser(), follow_redirects: bool = False
) -> ZIMServer:
    app = Flask(__name__)
    server = ZIMServer.from_path(app, path, parser)
    _connect_server(server, follow_redirects)
    return server


def create_server(
    dictionary: str, parser: Parser = DefaultParser(), follow_redirects: bool = False
) -> ZIMServer:
    app = Flask(__name__)
    server = ZIMServer.from_basedir(app, dictionary, parser)
    _connect_server(server, follow_redirects)
    return server


def serve_file(path: Path) -> None:
    server = create_server_for_path(path)
    server.start()
    print(f"Serving {str(path)} at {server.url}")
    server.join()
