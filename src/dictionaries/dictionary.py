from __future__ import annotations

import functools
import shutil
import string
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from bs4.element import NavigableString, PageElement, Tag
from zimply_core.zim_core import ZIMClient

from ..consts import USER_FILES
from ..errors import ZIMReaderException

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
    def __init__(self, name: str):
        folder_path = USER_FILES / name
        zim_path = next(folder_path.glob("*.zim"), None)
        if not zim_path:
            raise ZIMReaderException(f"No zim file was found in {str(name)}")
        self.zim_client = ZIMClient(
            zim_path,
            encoding="utf-8",
            auto_delete=True,
            # TODO: enable search support
            enable_search=False,
        )

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
        # FIXME: it's potentially unsafe to enable search support for now as the index is build in a separate thread and we're not keeping track of its progress
        # ZIMDict(name)

    @staticmethod
    @functools.lru_cache
    def get_soup(zim_client: ZIMClient, query: str) -> BeautifulSoup:
        article = zim_client.get_article(query)
        soup = BeautifulSoup(article.data.decode(), "html.parser")
        return soup

    def lookup(self, query: str, parser: Parser) -> DictEntry | None:
        query = strip_punct(query).strip()
        return parser.lookup(query, self)


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


PUNCT_TRANS_TABLE = str.maketrans("", "", string.punctuation)


def strip_punct(text: str) -> str:
    return text.translate(PUNCT_TRANS_TABLE)
