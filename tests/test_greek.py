from src.dictionaries.greek import GreekParser
from tests.utils import DictTester, strip_html


def test_greek() -> None:
    with DictTester("wiktionary_el_all_maxi", GreekParser(None)) as dictionary:
        entry = dictionary.lookup("γάτα")
        print(entry)
        assert (
            "(ζωολογία) κατοικίδιο τετράποδο θηλαστικό που ανήκει στην οικογένεια "
            in strip_html(entry.definitions[0])
        )
        assert "γάτα με πέταλα: πολύ ικανός και επιδέξιος άνθρωπος" in strip_html(
            entry.definitions[1]
        )
        assert strip_html(entry.pos) == "Ουσιαστικό Εκφράσεις"
        assert "αραβικά: قط" in strip_html(entry.translations)
        # assert "γάτες" in entry.inflections
