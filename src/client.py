"""
An abstraction layer over libzim and ZIMply
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Type

from .errors import ZIMClientLibNotAvailable


@dataclass
class ZIMItem:
    path: str
    title: str
    content: bytes
    mimetype: str


class ZIMClient(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def main_page(self) -> ZIMItem | None:
        raise NotImplementedError("Implement this to get the home page of the ZIM file")

    @abstractmethod
    def get_item_by_path(self, path: str) -> ZIMItem | None:
        raise NotImplementedError("Implement this to get an item given its path")

    @abstractmethod
    def get_item_by_title(self, title: str) -> ZIMItem | None:
        raise NotImplementedError("Implement this to get an article given its title")

    @abstractmethod
    def first_result(self, query: str) -> ZIMItem | None:
        raise NotImplementedError(
            "Implement this to return the first search result given a query"
        )


class ZIMplyClient(ZIMClient):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        try:
            from zimply_core.zim_core import ZIMClient

            self._zimply_client = ZIMClient(
                file_path,
                encoding="utf-8",
                auto_delete=True,
                enable_search=True,
            )
        except ImportError as exc:
            raise ZIMClientLibNotAvailable() from exc

    def _item_from_zimply_article(self, article: Any | None) -> ZIMItem | None:
        if not article:
            return None
        return ZIMItem(article.url, article.title, article.data, article.mimetype)

    def main_page(self) -> ZIMItem | None:
        return self._item_from_zimply_article(self._zimply_client.main_page)

    def get_item_by_path(self, path: str) -> ZIMItem | None:
        return self._item_from_zimply_article(self._zimply_client.get_article(path))

    def get_item_by_title(self, title: str) -> ZIMItem | None:
        return self._item_from_zimply_article(
            self._zimply_client.get_article_by_title(title)
        )

    def first_result(self, query: str) -> ZIMItem | None:
        results = self._zimply_client.search(query, 0, 1)
        if not results:
            return None
        return self.get_item_by_path(results[0].url)


class LibZIMClient(ZIMClient):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        try:
            from libzim.reader import Archive

            self._archive = Archive(file_path)
        except ImportError as exc:
            raise ZIMClientLibNotAvailable() from exc

    def _item_from_libzim_entry(self, entry: Any | None) -> ZIMItem | None:
        if not entry:
            return None
        return ZIMItem(
            entry.path,
            entry.title,
            bytes(entry.get_item().content),
            entry.get_item().mimetype,
        )

    def main_page(self) -> ZIMItem | None:
        return self._item_from_libzim_entry(self._archive.main_entry)

    def get_item_by_path(self, path: str) -> ZIMItem | None:
        return self._item_from_libzim_entry(self._archive.get_entry_by_path(path))

    def get_item_by_title(self, title: str) -> ZIMItem | None:
        return self._item_from_libzim_entry(self._archive.get_entry_by_title(title))

    def first_result(self, query: str) -> ZIMItem | None:
        from libzim.search import Query, Searcher

        query = Query().set_query(query)
        searcher = Searcher(self._archive)
        search = searcher.search(query)
        results = list(search.getResults(0, 1))
        if not results:
            return None
        return self.get_item_by_path(results[0])


def _get_available_client_class() -> Type[ZIMClient] | None:
    client_classes: list[Type[ZIMClient]] = [LibZIMClient, ZIMplyClient]
    for klass in client_classes:
        try:
            klass("")
        except ZIMClientLibNotAvailable:
            continue
        except:
            return klass
    return None


def init_client(zim_path: str | Path) -> ZIMClient:
    return _client_class(str(zim_path))


_client_class = _get_available_client_class()
assert _client_class
