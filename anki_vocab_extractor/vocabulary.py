"""Classes for representing vocabulary words and lists"""

# pyright: reportOptionalMemberAccess=false


import logging
from bs4 import NavigableString
from bs4.element import Tag
import pandas as pd

log = logging.getLogger(__name__)

class VocabularyWord:
    """A German word and its English translation, along with optional multimedia."""

    def __init__(
        self,
        german: str,
        translation: str,
        info: str = "",
        img: str = "",
        german_audio: str = "",
        register: str = "",
        example: str = "",
        example_audio: str = "",
        tags: str = "",
    ):
        self.german: str = german
        self.translation: str = translation
        self.info: str = info
        self.img: str = img
        self.german_audio: str = german_audio
        self.register: str = register
        self.example: str = example
        self.example_audio: str = example_audio
        self.tags: str = tags

    def __repr__(self) -> str:
        return f"VocabularyWord({self.german}, {self.translation})"

    def __eq__(self, other):
        return self.german == other.german

    def to_dict(self) -> dict:
        """Convert the VocabularyWord to a dictionary."""
        return {
            "german": self.german,
            "info": self.info,
            "translation": self.translation,
            "example": self.example,
            "register": self.register,
            "img": self.img,
            "german audio": self.german_audio,
            "example audio": self.example_audio,
        }

    @classmethod
    def from_html(cls, vocab_div: Tag):
        """Construct a VocabularyWord object from a BeautifulSoup div tag"""
        # Column 1: German words
        german_ctr = vocab_div.div
        if german_ctr is None:
            raise ValueError("No German word found in the vocabulary div")
        german = german_ctr.strong.string.strip().replace("|", "").strip()
        info = german_ctr.span.string.strip() if german_ctr.span else ""
        register = ""

        # Noun case
        if german.startswith(("der ", "die ", "das ")):
            register = "Substantiv"
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

        # Verb case
        elif info.split(", ")[-1].startswith("hat"):
            register = "Verb"
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

        # Adjective case
        elif info != "":
            register = "Adjektiv"

        # Expression/sentence case
        else:
            register = "Sonstiges"

        german_audio = str(german_ctr.audio) if german_ctr.audio else ""  # type: ignore

        # Column 2: Image (if exists)
        image_ctr = german_ctr.next_sibling
        img_tag = image_ctr.find("img", class_="hq-img")
        img = str(img_tag) if img_tag is not None else ""

        # Column 3: English translation
        translation_ctr = image_ctr.next_sibling
        if translation_ctr.span.p:
            translation = translation_ctr.span.p.string.strip()
        else:
            log.warning("No translation found for \"%s\"", german)
            translation = ""

        return cls(german, translation, info, img, german_audio, register)


class VocabularyList:
    """A list of VocabularyWord objects"""

    def __init__(self, vocabulary_words: list[VocabularyWord], title: str = ""):
        self.vocabulary_words: list[VocabularyWord] = vocabulary_words
        self.title: str = title

    def __repr__(self) -> str:
        return f"VocabularyList({self.vocabulary_words})"

    def __eq__(self, other):
        return self.vocabulary_words == other.vocabulary_words

    def to_df(self) -> pd.DataFrame:
        """Convert the VocabularyList to a pandas DataFrame."""
        return pd.DataFrame([word.to_dict() for word in self.vocabulary_words]).assign(
            tags=self.title.lower().replace(" ", "-")
        )

    @classmethod
    def from_html(cls, vocabulary_container: Tag | NavigableString, title: str = ""):
        """Construct a VocabularyList object from a BeautifulSoup ResultSet of div tags"""
        vocab_divs = vocabulary_container.find_all("div", recursive=False)
        vocabulary_words = []
        for vocab_div in vocab_divs:
            vocabulary_words.append(VocabularyWord.from_html(vocab_div))
        return cls(vocabulary_words, title)
