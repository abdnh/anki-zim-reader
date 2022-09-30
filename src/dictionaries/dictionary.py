from __future__ import annotations

import functools
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from bs4.element import NavigableString, PageElement, Tag
from zimply_core.zim_core import Article, ZIMClient

from ..consts import USER_FILES
from ..errors import ZIMReaderException
from .parser import DefaultParser

if TYPE_CHECKING:
    from .parser import Parser


@dataclass
class DictEntry:
    word: str
    definitions: list[str]
    examples: list[str]
    gender: str
    pos: str
    inflections: str
    translations: str


class ZIMDict:
    def __init__(self, name: str, parser: Parser = DefaultParser()):
        folder_path = USER_FILES / name
        zim_path = next(folder_path.glob("*.zim"), None)
        if not zim_path:
            raise ZIMReaderException(f"No zim file was found in {str(name)}")
        self.zim_client = ZIMClient(
            zim_path,
            encoding="utf-8",
            auto_delete=True,
            enable_search=True,
        )
        self.parser = parser

    @classmethod
    def build_dict(
        cls,
        filename: str | Path,
        name: str,
    ) -> None:
        # Copy input zim file to the output folder
        output_folder = USER_FILES / name
        output_folder.mkdir(exist_ok=True)
        shutil.copy(filename, output_folder)
        # Build search index
        ZIMDict(name)

    @staticmethod
    @functools.lru_cache
    def _get_soup(
        query: str, dictionary: ZIMDict, parser: Parser
    ) -> BeautifulSoup | None:
        article = parser.get_article(query, dictionary)
        soup = None
        if article:
            soup = BeautifulSoup(article.data.decode(), "html.parser")
        return soup

    def get_soup(self, query: str) -> BeautifulSoup | None:
        return self._get_soup(query, self, self.parser)

    def lookup(self, query: str) -> DictEntry | None:
        return self.parser.lookup(query, self)

    def get_article(self, query: str) -> Article | None:
        return self.parser.get_article(query, self)


def get_next_sibling_element(element: Tag) -> PageElement | None:
    sibling = element.next_sibling
    while isinstance(sibling, NavigableString):
        sibling = sibling.next_sibling
    return sibling


def get_prev_sibling_element(element: Tag) -> PageElement | None:
    sibling = element.previous_sibling
    while isinstance(sibling, NavigableString):
        sibling = sibling.previous_sibling
    return sibling


def strip_images(element: Tag) -> None:
    for img in element.find_all("img"):
        img.decompose()
