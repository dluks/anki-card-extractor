from dataclasses import dataclass

from anki_card_extractor.card import Card


@dataclass
class MonoglotAnxietyCard(Card):
    """A German word and its English translation, along with optional multimedia."""

    german: str = ""
    translation: str = ""
    info: str = ""
    img: str = ""
    german_audio: str = ""
    register: str = ""
    example: str = ""
    example_audio: str = ""
    tags: str = ""

    def __repr__(self) -> str:
        return (
            f"MonoglotAnxietyCard(german={self.german}, "
            f"translation={self.translation}, "
            f"info={self.info}, img={self.img}, "
            f"german_audio={self.german_audio}, "
            f"register={self.register}, "
            f"example={self.example}, "
            f"example_audio={self.example_audio}, "
            f"tags={self.tags})"
        )

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
