import re
from typing import List

from fuzzywuzzy import fuzz
from spellchecker import SpellChecker

from utils.book import Book


class BookSearch:
    def __init__(self, book: Book):
        self.book = book
        self.spellchecker = SpellChecker()

    @staticmethod
    def _remove_punctuation(text: str) -> str:
        pattern = r"[^a-zA-Z0-9\s]"
        return re.sub(pattern, "", text)

    def search(self, text: str, use_fuzz: bool = False) -> List[str]:
        # Spellcheck the text and suggest corrections
        corrected_words = []
        for word in self._remove_punctuation(text).split():
            corrected_word = self.spellchecker.correction(word.strip())
            corrected_word = corrected_word if corrected_word else word
            corrected_words.append(corrected_word)

        # Search for the corrected text in the book data
        pages_with_text = []
        if use_fuzz:
            for key, text_value in self.book.text.items():
                # Calculate the Levenshtein distance between the input text and the page text
                similarity = fuzz.token_set_ratio(text.lower(), text_value.lower())
                if similarity > 70:  # set a threshold of 70% similarity
                    pages_with_text.append(key)
        else:
            for key, text_value in self.book.text.items():
                if " ".join(corrected_words) in self._remove_punctuation(
                    text_value.lower()
                ):
                    pages_with_text.append(key)

        # Return the page number(s) where the text was found
        return pages_with_text
