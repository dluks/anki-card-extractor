import argparse
import os
from pathlib import Path

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
        default="flashcards",
    )

    args = parser.parse_args()

    # Make sure output directory exists
    args.output_dir = Path(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Parse the vocabulary
    vocab_parser = VocabularyParser(args.url)
    vocabulary_list = vocab_parser.extract_vocabulary()
    # print(vocabulary_list)

    # Generate the Anki cards
    card_generator = AnkiCardGenerator(vocabulary_list, args.output_dir)
    card_generator.generate_flashcards()

    print(f"Flashcards have been saved to {args.output_dir}")


if __name__ == "__main__":
    main()
