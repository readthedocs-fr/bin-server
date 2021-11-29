import unittest
import pygments
from bin import highlight

class TestHighlight(unittest.TestCase):
    @staticmethod
    def has_language_formatter(lang):
        try:
            pygments.lexers.get_lexer_by_name(lang)
            return True
        except pygments.util.ClassNotFound:
            return False

    def test_languages_has_formatter(self):
        for _ext, lang in highlight.languages:
            self.assertTrue(self.has_language_formatter(lang))
