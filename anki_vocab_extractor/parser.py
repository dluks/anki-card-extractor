"""Parses a "Wortzchatz" page on learngerman.dw.com to extract German vocabulary words
and their English translations."""

import requests
from bs4 import BeautifulSoup, NavigableString
from bs4.element import Tag

# pyright: reportOptionalMemberAccess=false


class VocabularyWord:
    """A German word and its English translation, along with optional multimedia."""

    def __init__(
        self,
        german_primary: str,
        translation: str,
        german_secondary: str | None = None,
        image_url: str | None = None,
        audio_url: str | None = None,
    ):
        self.german_primary: str = german_primary
        self.translation: str = translation
        self.german_secondary: str | None = german_secondary
        self.image_url: str | None = image_url
        self.audio_url: str | None = audio_url

    def __repr__(self) -> str:
        return f"VocabularyWord({self.german_primary}, {self.translation})"

    def __eq__(self, other):
        return self.german_primary == other.german_primary

    @classmethod
    def from_html(cls, vocab_div: Tag):
        """Construct a VocabularyWord object from a BeautifulSoup div tag"""
        # Column 1: German words
        german_ctr = vocab_div.div
        if german_ctr is None:
            raise ValueError("No German word found in the vocabulary div")
        cls.german_primary = german_ctr.strong.string.strip()
        cls.audio_url = german_ctr.audio.source["src"] if german_ctr.audio else None  # type: ignore
        cls.german_secondary = (
            german_ctr.span.string.strip() if german_ctr.span else None
        )

        # Column 2: Image (if exists)
        image_ctr = german_ctr.next_sibling
        cls.image_url = image_ctr.img["src"] if image_ctr.img else None

        # Column 3: English translation
        translation_ctr = image_ctr.next_sibling
        cls.translation = translation_ctr.span.p.string.strip()

        return cls


class VocabularyList:
    """A list of VocabularyWord objects"""

    def __init__(self, vocabulary_words: list[VocabularyWord]):
        self.vocabulary_words = vocabulary_words

    def __repr__(self) -> str:
        return f"VocabularyList({self.vocabulary_words})"

    def __eq__(self, other):
        return self.vocabulary_words == other.vocabulary_words

    @classmethod
    def from_html(cls, vocabulary_container: Tag | NavigableString):
        """Construct a VocabularyList object from a BeautifulSoup ResultSet of div tags"""
        vocab_divs = vocabulary_container.find_all("div", recursive=False)
        vocabulary_words = []
        for vocab_div in vocab_divs:
            vocabulary_words.append(VocabularyWord.from_html(vocab_div))
        return cls(vocabulary_words)


class VocabularyParser:
    """Extracts German vocabulary words and their English translations from a "Wortzchatz"
    page on learngerman.dw.com."""

    def __init__(self, url: str):
        self.url: str = url

    def extract_vocabulary(self) -> VocabularyList:
        """Extract German vocabulary words and their English translations from the URL."""
        # Make the HTTP request
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.content, "html.parser")

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
        vocabulary_list = VocabularyList.from_html(vocabulary_container)

        return vocabulary_list
