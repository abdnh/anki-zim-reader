from __future__ import annotations

from .dictionary import DictEntry, ZIMDict, save_images, strip_images
from .parser import Parser


class SpanishParser(Parser):
    """
    ZIM Parser for Spanish Wiktionary.
    Only tested with wiktionary_es_all_maxi_2022-07.
    Definition importing could use a lot of improvement.
    """

    name = "Spanish"

    # Spanish parts of speech used to detect parts of speech and definitions
    POS_LABELS = (
        "sustantivo",
        "nombre",
        "preposición",
        "pronombre",
        "verbo",
        "interjección",
        "conjunción",
        "adjetivo",
        "adverbio",
        "forma verbal",
        "forma sustantiva",
        "forma adjetiva",
        "participio",
        "artículo determinado",
        "expresión",
    )

    def lookup(self, query: str, dictionary: ZIMDict) -> DictEntry | None:
        soup = dictionary.get_soup(query)
        if not soup:
            return None
        pos: list[str] = []
        gender: list[str] = []
        definitions: list[str] = []
        inflections = ""
        translations = ""
        images: list[str] = []
        spanish_el = soup.select_one("#Español")
        if spanish_el:
            parent_details = spanish_el.find_parents("details")[0]
            inflection_table_el = parent_details.select_one(".inflection-table")
            if inflection_table_el:
                inflections = inflection_table_el.decode()
            imgs = save_images(dictionary, parent_details)
            images.extend(img.decode() for img in imgs)
            strip_images(parent_details)
            for entry in parent_details.select("details"):
                summary_el = entry.find("summary")
                translation_h = entry.select_one("#Traducciones")
                possible_pos = ""
                if summary_el:
                    spans = summary_el.find_all("span")
                    if spans:
                        possible_pos = spans[0].get_text()
                        if len(spans) >= 3:
                            gender.append(spans[2].get_text())
                    else:
                        possible_pos = summary_el.get_text()
                    summary_el.decompose()
                if any(l in possible_pos.lower() for l in self.POS_LABELS):
                    pos.append(possible_pos)
                elif translation_h:
                    translations = entry.decode_contents()
                    continue
                else:
                    continue
                # We're dumping all the entry contents here, which can include example sentences.
                # FIXME: find a consistent structure to parse this mess
                definitions.append(entry.decode_contents())

        return DictEntry(
            query,
            definitions,
            [],
            "<br>".join(gender),
            "<br>".join(pos),
            inflections,
            translations,
            "".join(images),
        )
