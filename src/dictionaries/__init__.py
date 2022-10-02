from __future__ import annotations

from pathlib import Path
from typing import Type

from ..consts import USER_FILES
from .dictionary import DictEntry, ZIMDict
from .german import GermanParser
from .greek import GreekParser
from .parser import DefaultParser, Parser
from .spanish import SpanishParser

PARSER_CLASSES: list[Type[Parser]] = [
    DefaultParser,
    GreekParser,
    SpanishParser,
    GermanParser,
]


def get_files() -> list[Path]:
    """Get a list of folder paths where imported ZIM files are stored"""
    return list(p for p in USER_FILES.iterdir() if p.is_dir())
