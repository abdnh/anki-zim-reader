import re
import shutil
import tempfile
from typing import Any

from src.dictionaries.dictionary import ZIMDict
from src.dictionaries.parser import Parser


class DictTester:
    def __init__(self, name: str, parser: Parser):
        self.base_dir = base_dir = tempfile.mkdtemp()
        print(base_dir)
        ZIMDict.build_dict(f"samples/{name}.zim", name, base_dir)
        self.dictionary = ZIMDict.from_basedir(name, parser, base_dir)

    def __enter__(self) -> ZIMDict:
        return self.dictionary

    def __exit__(self, exc: Any, value: Any, tb: Any) -> None:
        shutil.rmtree(self.base_dir, ignore_errors=True)


HTML_RE = re.compile(r"<.*?>")


def strip_html(html: str) -> str:
    return HTML_RE.sub("", html).replace("\xa0", "").strip()
