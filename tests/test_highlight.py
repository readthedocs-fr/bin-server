import unittest
import pygments
from bin import utils

class TestHighlight(unittest.TestCase):
    @staticmethod
    def has_language_formatter(lang):
        try:
            pygments.lexers.get_lexer_by_name(lang)
            return True
        except pygments.utils.ClassNotFound:
            return False

    def test_languages_has_formatter(self):
        for lang in utils.languages:
            self.assertTrue(self.has_language_formatter(lang[1]))
