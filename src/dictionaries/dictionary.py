from __future__ import annotations

import functools
import shutil
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from ..client import ZIMItem, init_client
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
    images: str
    ipa: str


class ZIMDict:
    def __init__(
        self,
        path: Path,
        parser: Parser = DefaultParser(),
    ):
        self.path = path
        self.client = init_client(path)
        self.parser = parser

    @classmethod
    def from_basedir(
        cls,
        name: str,
        parser: Parser = DefaultParser(),
        base_dir: Path | str = USER_FILES,
    ) -> ZIMDict:
        folder_path = Path(base_dir) / name
        zim_path = next(folder_path.glob("*.zim"), None)
        if not zim_path:
            raise ZIMReaderException(f"No zim file was found in {str(name)}")
        return ZIMDict(zim_path, parser)

    @classmethod
    def build_dict(
        cls,
        filename: Path | str,
        name: str,
        base_dir: Path | str = USER_FILES,
    ) -> None:
        # Copy input zim file to the output folder
        output_folder = Path(base_dir) / name
        output_folder.mkdir(exist_ok=True)
        shutil.copy(filename, output_folder)
        ZIMDict.from_basedir(name, base_dir=base_dir)

    @staticmethod
    @functools.lru_cache
    def _get_soup(
        title: str, dictionary: ZIMDict, parser: Parser
    ) -> BeautifulSoup | None:
        item = parser.get_item(title, dictionary, is_title=True)
        soup = None
        if item:
            soup = BeautifulSoup(item.content.decode(), "html.parser")
        return soup

    def get_soup(self, title: str) -> BeautifulSoup | None:
        return self._get_soup(title, self, self.parser)

    def lookup(self, title: str) -> DictEntry | None:
        if not title.strip():
            return None
        return self.parser.lookup(title, self)

    def get_item(self, path: str) -> ZIMItem | None:
        return self.parser.get_item(path, self)

    def save_resource(self, path: str) -> str | None:
        # Strip out '../'
        path = path.split("/", maxsplit=1)[-1]
        path = urllib.parse.unquote(path)
        try:
            item = self.client.get_item_by_path(path)
        except KeyError:
            return None
        filename = path.split("/")[-1]
        if self.parser.col:
            return self.parser.col.media.write_data(filename, item.content)
        return None


def get_next_sibling_element(element: Tag) -> Tag | None:
    sibling = element.next_sibling
    while isinstance(sibling, NavigableString):
        sibling = sibling.next_sibling
    return sibling


def get_prev_sibling_element(element: Tag) -> Tag | None:
    sibling = element.previous_sibling
    while isinstance(sibling, NavigableString):
        sibling = sibling.previous_sibling
    return sibling


def get_first_element_child(element: Tag) -> Tag | None:
    for child in element.children:
        if not isinstance(child, NavigableString):
            return child
    return None


def strip_images(element: Tag) -> None:
    for img in element.find_all("img"):
        img.decompose()


def save_images(dictionary: ZIMDict, element: Tag) -> list[Tag]:
    imgs = element.select(".thumbinner img")
    for img in imgs:
        src = img["src"]
        filename = dictionary.save_resource(src)
        if filename:
            img.attrs.clear()
            img["src"] = filename
    return imgs
