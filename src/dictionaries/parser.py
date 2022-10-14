"""A parser implements language-specific importing logic for a chosen dictionary source."""

from __future__ import annotations

import functools
import string
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ..client import ZIMItem

if TYPE_CHECKING:
    from anki.collection import Collection

    from .dictionary import DictEntry, ZIMDict


class Parser(ABC):
    name: str

    def __init__(self, col: Collection | None = None):
        self.col = col

    @staticmethod
    @functools.lru_cache
    def _get_item(
        path: str,
        dictionary: ZIMDict,
        is_title: bool,
    ) -> ZIMItem | None:
        get_item = (
            dictionary.client.get_item_by_title
            if is_title
            else dictionary.client.get_item_by_path
        )
        nopunct = path.strip(string.punctuation).strip()
        if is_title:
            forms = [path, nopunct, nopunct.lower(), nopunct.title(), nopunct.upper()]
        else:
            forms = [path, path, path.lower(), path.title(), path.upper()]
        for form in forms:
            try:
                item = get_item(form)
                return item
            except KeyError:
                pass
        return dictionary.client.first_result(path)

    def get_item(
        self, path: str, dictionary: ZIMDict, is_title: bool = False
    ) -> ZIMItem | None:
        return self._get_item(path, dictionary, is_title)

    @abstractmethod
    def lookup(self, query: str, dictionary: ZIMDict) -> DictEntry | None:
        raise NotImplementedError()

    def follow_redirects(self, query: str, dictionary: ZIMDict) -> str:
        """
        This can be implemented to get, for example, the non-inflected form of a word in
        which definitions and other contents exist.
        Useful for entries where there are only redirects to other entries, e.g. "See go" in the entry of "went".
        """
        return query


class DefaultParser(Parser):
    name = "Default"

    def lookup(self, query: str, dictionary: ZIMDict) -> DictEntry | None:
        return None
