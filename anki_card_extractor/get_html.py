"""Get HTML content from a URL."""

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_static_html(url: str) -> BeautifulSoup:
    """Fetches static HTML content from a URL using requests."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_rendered_html(url: str, headless: bool = True) -> BeautifulSoup:
    """Uses Playwright to fetch fully rendered HTML content from a URL."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        page.goto(url)

        page.wait_for_load_state("networkidle")

        # Optional: Wait for specific elements to load if lazy-loading requires them
        # page.wait_for_selector('.some-element')

        rendered_html = page.content()

        browser.close()

    return BeautifulSoup(rendered_html, "html.parser")


def get_html(url: str, rendered: bool = False) -> BeautifulSoup:
    """Fetches HTML content from a URL."""
    return get_rendered_html(url) if rendered else get_static_html(url)
