import unittest
from bin import txtparser


class TestTxtParser(unittest.TestCase):
    def test_ignore_comments(self):
        raw = "# Bonjour\nContenu\nEncore plus de contenu\n# Commentaire de nouveau\nFin du document"
        expected = [
            "Contenu",
            "Encore plus de contenu",
            "Fin du document"
        ]

        self.assertEqual(txtparser.parse(raw), expected)
