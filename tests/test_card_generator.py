# tests/test_card_generator.py
import unittest
import os
import csv
from anki_vocab_extractor.card_generator import AnkiCardGenerator


class TestAnkiCardGenerator(unittest.TestCase):
    def test_generate_flashcards(self):
        output_dir = "test_output"
        german_words = ["Hund", "Katze"]
        translations = ["Dog", "Cat"]

        # Generate the flashcards
        generator = AnkiCardGenerator(german_words, translations, output_dir)
        generator.generate_flashcards()

        # Check if the file was created
        file_path = os.path.join(output_dir, "anki_flashcards.csv")
        self.assertTrue(os.path.exists(file_path))

        # Check the contents of the file
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(rows[0], ["German", "Translation"])
            self.assertEqual(rows[1], ["Hund", "Dog"])
            self.assertEqual(rows[2], ["Katze", "Cat"])


if __name__ == "__main__":
    unittest.main()
