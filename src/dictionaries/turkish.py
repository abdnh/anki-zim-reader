from __future__ import annotations

from .dictionary import DictEntry, ZIMDict, save_images
from .parser import Parser


class TurkishParser(Parser):
    """
    ZIM Parser for Turkish Wiktionary.
    Tested with wiktionary_tr_all_maxi_2022-09.
    """

    name = "Turkish"

    def lookup(self, query: str, dictionary: ZIMDict) -> DictEntry | None:
        soup = dictionary.get_soup(query)
        if not soup:
            return None
        turkish_h = soup.select_one('[data-level="2"] [id*="Türkçe"]')
        if not turkish_h:
            return None
        turkish_details = turkish_h.parent.parent

        definitions = []
        examples = []
        pos_list = []
        inflection_tables = []
        translations = ""
        images = [img.decode() for img in save_images(dictionary, turkish_details)]
        ipa = []

        entries = turkish_details.select('details[data-level="3"]')
        # Some entries have data-level="4", and we detect them using the "headword" class
        for el in turkish_details.select(".headword"):
            entries.append(el.parent.parent)
        # FIXME: Some entries have data-level="4" but don't have "headword", like the entry of "yani".
        # Maybe a more consistent approach is to define a list of parts of speech that could occur and match against them,
        # like it's done for the Greek dictionary
        for entry in entries:
            example_els = entry.select("ol > li > dl")
            for el in example_els:
                examples.append(el.get_text())
                el.decompose()
            def_els = entry.select("ol > li, dl > dd")
            for el in def_els:
                definitions.append(el.get_text())
            pos_el = entry.select_one("summary")
            if pos_el and def_els:
                pos_list.append(pos_el.get_text())
                pos_el.decompose()

        inflection_els = turkish_details.select(".inflection-table")
        for el in inflection_els:
            inflection_tables.append(el.decode())

        translation_el = turkish_details.select_one(".çeviriler")
        if translation_el:
            translations = translation_el.decode()

        ipa = [el.get_text() for el in turkish_details.select(".IPA")]

        return DictEntry(
            query,
            definitions,
            examples,
            "",
            "<br>".join(pos_list),
            "<br>".join(inflection_tables),
            translations,
            "".join(images),
            " ".join(ipa),
        )
