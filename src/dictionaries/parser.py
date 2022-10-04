"""A parser implements language-specific importing logic for a chosen dictionary source."""

from __future__ import annotations

import functools
import string
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from zimply_core.zim_core import Article

if TYPE_CHECKING:
    from anki.collection import Collection

    from .dictionary import DictEntry, ZIMDict


class Parser(ABC):
    name: str

    def __init__(self, col: Collection | None = None):
        self.col = col

    @staticmethod
    @functools.lru_cache
    def _get_article(query: str, dictionary: ZIMDict) -> Article | None:
        query = query.strip(string.punctuation).strip()
        forms = [query, query.lower(), query.title(), query.upper()]
        for form in forms:
            try:
                article = dictionary.zim_client.get_article(form)
                return article
            except KeyError:
                pass
        # Return first search result, if any
        results = dictionary.zim_client.search(query, 0, 1)
        if results:
            return dictionary.zim_client.get_article(results[0].url)
        return None

    def get_article(self, query: str, dictionary: ZIMDict) -> Article | None:
        return self._get_article(query, dictionary)

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
