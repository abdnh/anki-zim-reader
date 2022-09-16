from __future__ import annotations

from pathlib import Path
from typing import Type

from ..consts import USER_FILES
from .dictionary import DictEntry, DictException, ZIMDict
from .greek import GreekParser
from .parser import Parser
from .spanish import SpanishParser

PARSER_CLASSES: list[Type[Parser]] = [GreekParser, SpanishParser]


def get_files() -> list[Path]:
    """Get a list of folder paths where imported ZIM files are stored"""
    return list(p for p in USER_FILES.iterdir() if p.is_dir())
