# anki_vocab_extractor/card_generator.py
import csv
import os


class AnkiCardGenerator:
    def __init__(self, german_words, translations, output_dir):
        self.german_words = german_words
        self.translations = translations
        self.output_dir = output_dir

    def generate_flashcards(self):
        file_path = os.path.join(self.output_dir, "anki_flashcards.csv")
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["German", "Translation"])  # Header row

            for german_word, translation in zip(self.german_words, self.translations):
                writer.writerow([german_word, translation])
