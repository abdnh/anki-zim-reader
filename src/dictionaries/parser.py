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
