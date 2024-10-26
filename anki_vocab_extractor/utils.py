"""Utility functions for the Anki Card Extractor."""

from bs4 import PageElement, Tag


def bs4tag(tag: PageElement | None) -> Tag:
    """Check if a bs4.element.Tag is a Tag object."""
    if not isinstance(tag, Tag):
        raise ValueError("Not a Tag object")
    return tag


def bs4str(string: str | None) -> str:
    """Check if a BS4 Tag.string is not None."""
    if string is None:
        raise ValueError("String is None")
    return string
