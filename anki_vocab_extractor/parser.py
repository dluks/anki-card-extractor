"""Parses a "Wortzchatz" page on learngerman.dw.com to extract German vocabulary words
and their English translations."""

# pyright: reportOptionalMemberAccess=false
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from anki_vocab_extractor.card import CardList


class CardParser(ABC):
    """Abstract base class for parsing cards from a webpage."""

    def __init__(self, html: str):
        self.html: str = html

    @abstractmethod
    def extract_cards(self) -> CardList:
        """Extract cards from the HTML content."""


class LearnGermanCardParser(CardParser):
    """Extracts German vocabulary words and their English translations from a "Wortzchatz"
    page on learngerman.dw.com."""

    def extract_cards(self) -> CardList:
        """Extract German vocabulary words and their English translations from the URL."""
        # Parse the HTML
        soup = BeautifulSoup(self.html, "html.parser")

        section_title = soup.find("section", id="lesson").h1.string.strip()

        knowledge_wrapper = soup.find("div", class_="knowledge-wrapper")
        if not knowledge_wrapper:
            raise ValueError("No 'knowledge-wrapper' div found on the page")

        # Step 4: Find the classless div inside the 'knowledge-wrapper' (which contains
        # the vocabulary divs)
        vocabulary_container = knowledge_wrapper.find(
            "div", class_=None
        )  # Finds the first classless div
        if not vocabulary_container:
            raise ValueError("No vocabulary container found inside 'knowledge-wrapper'")

        # Extract German words and their English translations
        card_list = CardList.from_html(vocabulary_container, section_title)

        return card_list
