"""Parses a "Wortzchatz" page on learngerman.dw.com to extract German vocabulary words
and their English translations."""

# pyright: reportOptionalMemberAccess=false
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from anki_vocab_extractor.vocabulary import VocabularyList


class VocabularyParser:
    """Extracts German vocabulary words and their English translations from a "Wortzchatz"
    page on learngerman.dw.com."""

    def __init__(self, url: str, headless: bool = True):
        self.url: str = url
        self.headless: bool = headless

    def get_rendered_html(self):
        """Uses Playwright to fetch fully rendered HTML including lazy-loaded content"""
        # Initialize Playwright and open the browser
        with sync_playwright() as p:
            # Choose the browser (Chromium is used here)
            browser = p.chromium.launch(
                headless=self.headless
            )  # Use headless=True to run without a GUI
            page = browser.new_page()

            # Step 1: Navigate to the URL
            page.goto(self.url)

            # Step 2: Wait for page content to load, you can also target specific elements
            page.wait_for_load_state(
                "networkidle"
            )  # Wait until the network is idle (no requests for 500ms)

            # Optional: Wait for specific elements to load if lazy-loading requires them
            # page.wait_for_selector('.some-element')

            # Step 3: Get the fully rendered HTML
            rendered_html = (
                page.content()
            )  # This fetches the fully rendered HTML after JavaScript execution

            # Step 4: Close the browser
            browser.close()

        return rendered_html

    def extract_vocabulary(self) -> VocabularyList:
        """Extract German vocabulary words and their English translations from the URL."""
        rendered_html = self.get_rendered_html()

        # Parse the HTML
        soup = BeautifulSoup(rendered_html, "html.parser")

        vocabulary_title = soup.find("section", id="lesson").h1.string.strip()

        knowledge_wrapper = soup.find("div", class_="knowledge-wrapper")
        if not knowledge_wrapper:
            raise ValueError("No 'knowledge-wrapper' div found on the page")

        # Step 4: Find the classless div inside the 'knowledge-wrapper' (which contains
        # the vocabulary divs)
        vocabulary_container = knowledge_wrapper.find(
            "div", class_=None
        )  # Finds the first classless div
        if not vocabulary_container:
            raise ValueError("No vocabulary container found inside 'knowledge-wrapper'")

        # Extract German words and their English translations
        vocabulary_list = VocabularyList.from_html(
            vocabulary_container, vocabulary_title
        )

        return vocabulary_list
