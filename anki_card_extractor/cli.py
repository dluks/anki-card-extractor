"""Command line interface for the Anki card extractor."""

import argparse
from pathlib import Path

from anki_card_extractor.get_html import get_html

from .card_generator import MonoglotAnxietyCardGenerator
from .parsers.learngerman import LearnGermanVocabParser


def main():
    """Extract Anki cards from a webpage and generate Anki importable flashcards."""
    parser = argparse.ArgumentParser(
        description="Extract Anki cards from a webpage and generate importable flashcards."
    )
    parser.add_argument(
        "url", type=str, help="URL of the webpage to extract cards from"
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

    # Parse the html and extract cards
    html = get_html(args.url, rendered=True)
    html_parser = LearnGermanVocabParser(html)
    card_list = html_parser.extract_cards()

    # Generate the Anki cards
    card_generator = MonoglotAnxietyCardGenerator(card_list, "Deutsch", args.output_dir)
    card_generator.generate_flashcards()

    print(f"Flashcards have been saved to {args.output_dir}")


if __name__ == "__main__":
    main()
