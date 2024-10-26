"""Parses a "Wortzchatz" page on learngerman.dw.com to extract German vocabulary words
and their English translations."""

from abc import ABC, abstractmethod

from bs4 import BeautifulSoup, Tag

from .card import Card, CardList


class HTMLParser(ABC):
    """Abstract base class for parsing cards from a webpage."""

    def __init__(self, soup: BeautifulSoup):
        self.soup: BeautifulSoup = soup

    @abstractmethod
    def _extract_card(self, card_ctr: Tag) -> Card:
        """Extract a card from a bs4 Tag."""
        raise NotImplementedError

    @abstractmethod
    def extract_cards(self, card_type: Card) -> CardList:
        """Extract cards from the HTML content."""
        raise NotImplementedError
