"""Description: Generates Anki flashcards from a list of German words and their English
translations"""

from pathlib import Path

from anki_vocab_extractor.card import CardList


class AnkiCardGenerator:
    """Generates Anki flashcards from a list of German words and their English translations"""

    def __init__(self, card_list: CardList, output_dir: Path):
        self.card_list: CardList = card_list
        self.output_dir: Path = output_dir

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
            f.write("#deck:Deutsch\n")
            f.write(f"#tags column:{len(df.columns)}\n")

        # Append the DataFrame to the file
        df.to_csv(
            file_path, index=False, sep=";", encoding="utf-8", header=False, mode="a"
        )
