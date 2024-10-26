"""Classes for representing vocabulary words and lists"""

# pyright: reportOptionalMemberAccess=false


import logging
from abc import ABC, abstractmethod

import pandas as pd

log = logging.getLogger(__name__)


class Card(ABC):
    """Abstract base class for representing a vocabulary card"""

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the card to a dictionary"""
        raise NotImplementedError


class CardList:
    """A list of Cards"""

    def __init__(self, cards: list[Card], title: str = ""):
        self.cards: list[Card] = cards
        self.title: str = title

    def __repr__(self) -> str:
        return f"CardList({self.cards})"

    def __eq__(self, other):
        return self.cards == other.cards

    def to_df(self) -> pd.DataFrame:
        """Convert the VocabularyList to a pandas DataFrame."""
        return pd.DataFrame([word.to_dict() for word in self.cards]).assign(
            tags=self.title.lower().replace(" ", "-")
        )
