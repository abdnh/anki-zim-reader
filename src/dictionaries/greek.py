from __future__ import annotations

import re
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

from .dictionary import DictEntry, ZIMDict, strip_images
from .parser import Parser

if TYPE_CHECKING:
    from spacy.language import Language


class GreekParser(Parser):
    """
    ZIM Parser for Greek Wiktionary.
    Only tested with wiktionary_el_all_maxi_2022-07.zim and has many issues.
    """

    name = "Greek"

    def __init__(self) -> None:
        self.nlp: Language | None = None
        try:
            import spacy

            self.nlp = spacy.load("el_core_news_sm")
        except:
            pass
        super().__init__()

    def _stem(self, word: str) -> str:
        doc = self.nlp(word)
        lemmas = []
        for token in doc:
            lemmas.append(token.lemma_)
        return " ".join(lemmas)

    # HTML IDs one of which is assumed to exist in the queried page
    LANG_IDS = (
        r"#Ελληνικά_\(el\)",
        r"#Αρχαία_ελληνικά_\(grc\)",
        r"#Μεσαιωνικά_ελληνικά_\(gkm\)",
    )

    # Greek parts of speech used to detect parts of speech and definitions
    POS_LABELS = (
        "άρθρο",
        "ουσιαστικό",
        "επίθετο",
        "αντωνυμία",
        "ρήμα",
        "κλιτή μετοχή",
        "άκλιτη μετοχή",
        "επίρρημα",
        "σύνδεσμος",
        "πρόθεση",
        "επιφώνημα",
        "ρηματικός τύπος",
        "επιθέτου",
        "ουσιαστικού",
        "αριθμητικό",
        "συντομομορφή",
        "αριθμητικού",
        "όνομα",
        "μετοχή",
        "μόριο",
        "αντωνυμία",
        "μετοχής",
        "προστακτική",
        "εκφράσεις",
        "αντωνυμίας",
    )

    # A tuple of regexes used to detect redirects and bools used to decide whether to merge the current entry definitions with the redirected-to entry (incomplete)
    REDIRECT_PATTERNS = tuple(
        (re.compile(s), merge)
        for (s, merge) in (
            (r"ενικό.*?του ρήματος\s+(.*)", False),
            (r"υποκοριστικό.*?του\s+(.*)", False),
            (r"(?:(?:θηλυκό)|(?:αρσενικό)|(?:ουδέτερο)).*?του\s+(\w+)", False),
            (r"(.*?),.*?του.*?ενικού", False),
            (r"(.*?),.*?του.*?πληθυντικού", False),
            (r"το.*?αποτέλεσμα.*?του\s+(.*)", True),
        )
    )

    def _get_soup(self, query: str, dictionary: ZIMDict) -> BeautifulSoup | None:
        forms = [query, query.lower(), query.title(), query.upper()]
        if self.nlp:
            forms.append(self._stem(query))
        soup = None
        for form in forms:
            try:
                soup = dictionary.get_soup(dictionary.zim_client, form)
                break
            except KeyError:
                pass
        return soup

    def follow_redirects(self, query: str, dictionary: ZIMDict) -> str:
        soup = self._get_soup(query, dictionary)
        if not soup:
            return query
        greek_el = None
        for lang_id in self.LANG_IDS:
            greek_el = soup.select_one(lang_id)
            if greek_el:
                break
        if greek_el:
            parent_details = greek_el.find_parents("details")[0]
            for entry in parent_details.select("details"):
                entry_text = entry.get_text()
                redirect_word = None
                for (redirect_pattern, _) in self.REDIRECT_PATTERNS:
                    match = redirect_pattern.search(entry_text)
                    if match:
                        redirect_word = match.group(1)
                        break
                if redirect_word:
                    return self.follow_redirects(redirect_word, dictionary)
        return query

    def lookup(self, query: str, dictionary: ZIMDict) -> DictEntry | None:
        soup = self._get_soup(query, dictionary)
        if not soup:
            return None
        pos: list[str] = []
        gender: list[str] = []
        definitions: list[str] = []
        inflections = ""
        translations = ""
        greek_el = None
        for lang_id in self.LANG_IDS:
            greek_el = soup.select_one(lang_id)
            if greek_el:
                break
        if greek_el:
            parent_details = greek_el.find_parents("details")[0]
            inflection_table_el = parent_details.select_one("table")
            if inflection_table_el:
                inflections = inflection_table_el.decode()
            for entry in parent_details.select("details"):
                strip_images(entry)
                summary_el = entry.find("summary")
                translation_h = entry.select_one("#Μεταφράσεις")
                if summary_el:
                    possible_pos = summary_el.get_text()
                    summary_el_title = summary_el.get("title", "")
                    if any(
                        l.lower() in possible_pos.lower() for l in self.POS_LABELS
                    ) or any(
                        l.lower() in summary_el_title.lower() for l in self.POS_LABELS
                    ):
                        pos.append(possible_pos)
                    elif translation_h:
                        translations = entry.decode_contents()
                        continue
                    else:
                        continue
                    summary_el.decompose()
                # Try to detect redirects from variants like plurals to the page of the base words where the actual definitions are.
                # FIXME: should we only follow redirects if we find a single definition?
                redirect_word = None
                should_merge = False
                entry_text = entry.get_text()
                for (redirect_pattern, merge) in self.REDIRECT_PATTERNS:
                    match = redirect_pattern.search(entry_text)
                    if match:
                        redirect_word = match.group(1)
                        should_merge = merge
                        break
                if redirect_word:
                    redirect_dictentry = self.lookup(redirect_word, dictionary)
                    if should_merge:
                        redirect_dictentry.definitions = [
                            entry.decode_contents()
                        ] + redirect_dictentry.definitions
                    return redirect_dictentry
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
        )
