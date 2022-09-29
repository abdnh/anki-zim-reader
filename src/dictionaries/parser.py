"""A parser implements language-specific importing logic for a chosen dictionary source."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dictionary import DictEntry, ZIMDict


class Parser(ABC):
    name: str

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
