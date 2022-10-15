from __future__ import annotations

import re

from .dictionary import (
    DictEntry,
    ZIMDict,
    get_first_element_child,
    get_next_sibling_element,
    save_images,
)
from .parser import Parser


class GermanParser(Parser):
    """
    ZIM Parser for German Wiktionary.
    Tested with wiktionary_de_all_maxi_2022-09.zim.
    """

    name = "German"

    def lookup(self, query: str, dictionary: ZIMDict) -> DictEntry | None:
        soup = dictionary.get_soup(query)
        if not soup:
            return None

        german_h = soup.select_one('[data-level="2"] [id*="Deutsch"]')
        if not german_h:
            return None
        german_details = german_h.parent.parent

        definitions = []
        examples = []
        pos_list = []
        gender_list = []
        inflections_list = []
        translations_list = []
        images: list[str] = []

        entries = german_details.select('details[data-level="3"]')
        for entry in entries:
            meaning_sects = entry.select('[title="Sinn und Bezeichnetes (Semantik)"]')
            for sect in meaning_sects:
                dl = get_next_sibling_element(sect)
                for dd in dl.select("dd"):
                    definitions.append(dd.decode_contents())

            example_sects = entry.select('[title="Verwendungsbeispielsätze"]')
            for sect in example_sects:
                dl = get_next_sibling_element(sect)
                for dd in dl.select("dd"):
                    examples.append(dd.decode_contents())

            pos_gender_h = get_first_element_child(entry).select_one("h3")
            pos_list.append(pos_gender_h.get_text().split(",")[0])
            gender_el = pos_gender_h.select_one("em")
            if gender_el:
                if re.match(r"Genus: (.*)", gender_el["title"]):
                    gender_list.append(gender_el.get_text())

            inflection_table = entry.select_one(".inflection-table")
            if inflection_table:
                inflections_list.append(inflection_table.decode())

            imgs = save_images(dictionary, entry)
            images.extend(img.decode() for img in imgs)

        translations_table = german_details.select_one('[title*="Übersetzungen"]')
        if translations_table:
            translations_list.append(translations_table.decode())

        return DictEntry(
            query,
            definitions,
            examples,
            "<br>".join(gender_list),
            "<br>".join(pos_list),
            "<br>".join(inflections_list),
            "<br>".join(translations_list),
            "".join(images),
        )
