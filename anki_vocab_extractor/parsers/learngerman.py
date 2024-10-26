"""Extracts German -> English vocabulary from a "Wortschatz" page on learngerman.dw.com."""

import logging

from bs4 import BeautifulSoup, Tag

from anki_vocab_extractor.card import CardList
from anki_vocab_extractor.cards.monoglotanxiety import MonoglotAnxietyCard
from anki_vocab_extractor.html_parser import HTMLParser
from anki_vocab_extractor.utils import bs4str, bs4tag

log = logging.getLogger(__name__)


class LearnGermanVocabParser(HTMLParser):
    """Extracts German vocabulary words and their English translations from a "Wortzchatz"
    page on learngerman.dw.com."""

    def __init__(self, soup: BeautifulSoup):
        super().__init__(soup)
        self.section_title = self._parse_section_title()

    def _parse_section_title(self) -> str:
        """Parse the title of the vocabulary section."""
        return bs4str(bs4tag(self.soup.select_one("section#lesson h1")).string).strip()

    def _card_main(self, german_ctr: Tag) -> tuple[str, str, str]:
        """Extract the main information from the card."""
        german = (
            bs4str(bs4tag(german_ctr.strong).string).strip().replace("|", "").strip()
        )
        info = bs4str(german_ctr.span.string).strip() if german_ctr.span else ""
        register = self._get_register(german, info)

        match register:
            case "Substantiv":
                german, info = self._extract_noun(german, info)
            case "Verb":
                german, info = self._extract_verb(german, info)
            case "Adjektiv":
                pass
            case "Sonstiges":
                pass

        return german, info, register

    def _card_media(self, german_ctr: Tag, image_ctr: Tag) -> tuple[str, str]:
        """Extract media from the card."""
        img_tag = image_ctr.find("img", class_="hq-img")
        img = str(img_tag) if img_tag is not None else ""
        german_audio = str(german_ctr.audio) if german_ctr.audio else ""
        return img, german_audio

    def _extract_card(self, card_ctr: Tag) -> MonoglotAnxietyCard:
        """Extract a vocabulary item from the page."""
        german_ctr = bs4tag(card_ctr.div)
        image_ctr = bs4tag(german_ctr.next_sibling)
        translation_ctr = bs4tag(image_ctr.next_sibling)

        german, info, register = self._card_main(german_ctr)
        translation = bs4tag(translation_ctr.span)
        if translation.p is None:
            translation = ""
            log.warning("Translation not found for %s", german)
        else:
            translation = bs4str(translation.p.string).strip()
        img, german_audio = self._card_media(german_ctr, image_ctr)

        return MonoglotAnxietyCard(
            german=german,
            translation=translation,
            info=info,
            img=img,
            german_audio=german_audio,
            register=register,
        )

    def extract_cards(self, card_type=MonoglotAnxietyCard) -> CardList:
        """Extract vocabulary items on the page."""
        vocab_items = bs4tag(
            bs4tag(self.soup.select_one("div.knowledge-wrapper")).find(
                "div", class_=None
            )
        ).find_all("div", recursive=False)

        card_list = CardList([], self.section_title)
        for vocab_item in vocab_items:
            if not isinstance(vocab_item, Tag):
                continue

            vocab_card = self._extract_card(vocab_item)
            card_list.cards.append(vocab_card)

        if not card_list.cards:
            raise ValueError("No cards found on the page")

        return card_list

    @staticmethod
    def _get_register(german: str, info: str) -> str:
        """Determine the part of speech of the vocabulary item."""
        if german.startswith(("der ", "die ", "das ")):
            return "Substantiv"
        if info.split(", ")[-1].startswith("hat"):
            return "Verb"
        if info != "":
            return "Adjektiv"
        return "Sonstiges"

    @staticmethod
    def _extract_noun(
        german: str,
        info: str,
    ) -> tuple[str, str]:
        parts = german.split(", ")
        german = parts[0].strip()
        info_from_german = parts[1].strip() if len(parts) > 1 else ""

        if info:
            info = (
                f"{info_from_german}<br><br><i>{info}</i>"
                if info_from_german
                else f"<i>{info}</i>"
            )
        else:
            info = info_from_german

        return german, info

    @staticmethod
    def _extract_verb(german: str, info: str) -> tuple[str, str]:
        if german.startswith("sich"):
            # Add "sich" after the conjugations in secondary
            parts = info.split(", ")
            parts = [
                (
                    f"{part} sich"
                    if i != 2
                    else f"{part.split()[0]} sich {part.split()[1]}"
                )
                for i, part in enumerate(parts)
            ]
            info = ", ".join(parts)

        if german.split("sich ")[-1].startswith("etwas"):
            # Remove "etwas" from the primary
            german = "".join(german.split("etwas "))

        return german, info
