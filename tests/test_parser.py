import unittest
from unittest.mock import patch

from anki_vocab_extractor.parser import VocabularyParser


class TestVocabularyParser(unittest.TestCase):
    @patch("requests.get")
    def test_extract_vocabulary(self, mock_get):
        # Mock HTML content
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = """
        <div class="sc-erIdjD">
            <div class="sc-ewnqHT">Hund</div>
            <div class="sc-bxiBER">Dog</div>
        </div>
        <div class="sc-erIdjD">
            <div class="sc-ewnqHT">Katze</div>
            <div class="sc-bxiBER">Cat</div>
        </div>
        """

        vocab_parser = VocabularyParser("http://mocked-url.com")
        german_words, translations = vocab_parser.extract_vocabulary()

        self.assertEqual(german_words, ["Hund", "Katze"])
        self.assertEqual(translations, ["Dog", "Cat"])


if __name__ == "__main__":
    unittest.main()
