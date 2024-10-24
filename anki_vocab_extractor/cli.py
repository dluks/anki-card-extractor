import argparse
import os

from .parser import VocabularyParser
from .card_generator import AnkiCardGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Extract vocabulary from a webpage and generate Anki flashcards."
    )
    parser.add_argument(
        "url", type=str, help="URL of the webpage to extract vocabulary from"
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        help="Directory to store the Anki flashcards",
        default="output",
    )

    args = parser.parse_args()

    # Make sure output directory exists
    # os.makedirs(args.output_dir, exist_ok=True)

    # Parse the vocabulary
    vocab_parser = VocabularyParser(args.url)
    vocabulary_list = vocab_parser.extract_vocabulary()
    print(vocabulary_list)

    # Generate the Anki cards
    # card_generator = AnkiCardGenerator(german_words, translations, args.output_dir)
    # card_generator.generate_flashcards()

    # print(f"Flashcards have been saved to {args.output_dir}")


if __name__ == "__main__":
    main()
