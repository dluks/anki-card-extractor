"""Test the LearnGermanVocabParser class."""

# pylint: disable=redefined-outer-name
import re

import pytest
from bs4 import BeautifulSoup

from anki_card_extractor.card import CardList
from anki_card_extractor.cards.monoglotanxiety import MonoglotAnxietyCard
from anki_card_extractor.parsers.learngerman import LearnGermanVocabParser


@pytest.fixture
def sample_soup():
    """Read sample_html_learngerman.html and return its contents."""
    with open("tests/sample_html_learngerman.html", "r", encoding="utf-8") as file:
        # Remove all types of whitespace using regex
        clean_html = re.sub(r">\s+<", "><", file.read())
    return BeautifulSoup(clean_html, "html.parser")


def test_extract_cards(sample_soup):
    """Test the LearnGermanVocabParser.extract_cards() method."""
    parser = LearnGermanVocabParser(sample_soup)
    card_list = parser.extract_cards()
    assert isinstance(card_list, CardList)
    assert card_list.title == "Praktisch!"
    assert len(card_list.cards) == 9

    # Noun card
    noun_card = card_list.cards[0]
    assert isinstance(noun_card, MonoglotAnxietyCard)
    assert noun_card.register == "Substantiv"
    assert noun_card.german == "die Bibel"
    assert noun_card.info == "die Bibeln"
    assert noun_card.translation == "Bible"
    assert (
        noun_card.img
        == """<img alt="die Bibel, die Bibeln" class="hq-img loaded" src="https://static.dw.com/image/40244638_602.jpg"/>"""
    )
    assert (
        noun_card.german_audio
        == """<audio tabindex="0" width="100%"><source src="https://radiodownloaddw-a.akamaihd.net/Events/dwelle/deutschkurse/nicosweg/wortschatz/BAKU_A2_Bibel.mp3" type="audio/MP3"/></audio>"""
    )

    # Verb card
    verb_card = card_list.cards[1]
    assert isinstance(verb_card, MonoglotAnxietyCard)
    assert verb_card.register == "Verb"
    assert verb_card.german == "jemanden an etwas beteiligen"
    assert verb_card.info == "beteiligt, beteiligte, hat beteiligt"
    assert (
        verb_card.translation
        == "to include someone in something; to involve someone in something"
    )

    # Adjective card
    adj_card = card_list.cards[2]
    assert isinstance(adj_card, MonoglotAnxietyCard)
    assert adj_card.register == "Adjektiv"
    assert adj_card.german == "flach"
    assert adj_card.info == "flacher, am flachsten"
    assert adj_card.translation == "flat"

    # Other card
    other_card = card_list.cards[3]
    assert isinstance(other_card, MonoglotAnxietyCard)
    assert other_card.register == "Sonstiges"
    assert other_card.german == "absolut"
    assert other_card.info == ""
    assert other_card.translation == "absolute/absolutely"

    # Reflexive verb card
    refl_verb_card = card_list.cards[4]
    assert isinstance(refl_verb_card, MonoglotAnxietyCard)
    assert refl_verb_card.register == "Verb"
    assert refl_verb_card.german == "sich wünschen"
    assert refl_verb_card.info == "wünscht sich, wünschte sich, hat sich gewünscht"
    assert refl_verb_card.translation == "to make a wish"

    # Empty translation card
    empty_trans_card = card_list.cards[5]
    assert isinstance(empty_trans_card, MonoglotAnxietyCard)
    assert empty_trans_card.register == "Substantiv"
    assert empty_trans_card.german == "das Fernsehen"
    assert empty_trans_card.info == "<i>nur Singular</i>"
    assert empty_trans_card.translation == ""

    # B1 noun card
    b1_noun_card = card_list.cards[6]
    assert isinstance(b1_noun_card, MonoglotAnxietyCard)
    assert b1_noun_card.register == "Substantiv"
    assert b1_noun_card.german == "der Arbeitsmarkt, -märkte"
    assert b1_noun_card.info == ""
    assert b1_noun_card.translation == "alle Arbeitsstellen (z. B. in einer Stadt)"

    # B1 nur Singular noun card
    b1_sing_noun_card = card_list.cards[7]
    assert isinstance(b1_sing_noun_card, MonoglotAnxietyCard)
    assert b1_sing_noun_card.register == "Substantiv"
    assert b1_sing_noun_card.german == "das Arbeitslosengeld"
    assert b1_sing_noun_card.info == "<i>nur Singular</i>"
    assert (
        b1_sing_noun_card.translation
        == "das Geld, das man vom Staat bekommt, wenn man arbeitslos ist"
    )

    # B1 role noun card
    b1_role_noun_card = card_list.cards[8]
    assert isinstance(b1_role_noun_card, MonoglotAnxietyCard)
    assert b1_role_noun_card.register == "Substantiv"
    assert b1_role_noun_card.german == "Berater, -/Beraterin, -nen"
    assert b1_role_noun_card.info == ""
    assert (
        b1_role_noun_card.translation
        == "jemand, der anderen Menschen mit seinem Wissen hilft oder Tipps gibt"
    )
