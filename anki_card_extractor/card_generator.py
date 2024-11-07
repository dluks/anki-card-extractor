"""Description: Generates Anki flashcards from a list of German words and their English
translations"""

from abc import ABC
from pathlib import Path

from .card import CardList


class CardGenerator(ABC):
    """Abstract base class for generating Anki flashcards"""

    def __init__(self, card_list: CardList, deck: str, output_dir: Path):
        self.card_list: CardList = card_list
        self.deck: str = deck
        self.output_dir: Path = output_dir

    def generate_flashcards(self):
        """Generate Anki flashcards and save them to a file"""
        raise NotImplementedError


class MonoglotAnxietyCardGenerator(CardGenerator):
    """Generates Anki flashcards per the Monoglot Anxiety note type"""

    def generate_flashcards(self):
        """Generate Anki flashcards and save them to a CSV file"""
        file_path = self.output_dir / "anki_flashcards.csv"
        df = self.card_list.to_df()
        # Write the header information to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#separator:;\n")
            f.write("#html:true\n")
            columns = ";".join(df.columns)
            f.write(f"#columns:{columns}\n")
            f.write("#notetype:Monoglot Anxiety\n")
            f.write(f"#deck:{self.deck}\n")
            f.write(f"#tags column:{len(df.columns)}\n")

        # Append the DataFrame to the file
        df.to_csv(
            file_path, index=False, sep=";", encoding="utf-8", header=False, mode="a"
        )
