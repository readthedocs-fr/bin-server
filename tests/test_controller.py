import bottle
import signal
import unittest
import urllib.request as urlreq
from bin import config
from bin.models import Snippet
from bottle import template as bottle_template
from html.parser import HTMLParser
from threading import Thread
from unittest.mock import patch, MagicMock


snippet_lipsum = Snippet(ident='lipsum', code="Lipsum", views_left=float('+inf'))
snippet_python = Snippet(ident='egg', code='print("Hello world")', views_left=float('+inf'))


class HTMLSanitizer(HTMLParser):
    def __init__(self, assertEqual, assertIn):
        self.assertIn = assertIn
        self.assertEqual = assertEqual
        self.pairtags = {
            'a', 'abbr', 'acronym', 'address', 'applet', 'article',
            'aside', 'audio', 'b', 'basefont', 'bdi', 'bdo', 'big',
            'blockquote', 'body', 'button', 'canvas', 'caption',
            'center', 'cite', 'code', 'colgroup', 'data', 'datalist',
            'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt',
            'em', 'fieldset', 'figcaption', 'figure', 'font',
            'footer', 'form', 'frame', 'frameset', 'head', 'header', 'hgroup',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'html', 'i', 'iframe',
            'ins', 'kbd', 'label', 'legend', 'li',
            'main', 'map', 'mark', 'menu', 'menuitem', 'meter',
            'nav', 'noframes', 'noscript', 'object', 'ol', 'optgroup',
            'option', 'output', 'p', 'picture', 'pre', 'progress',
            'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section',
            'select', 'small', 'span', 'strike', 'strong', 'style',
            'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template',
            'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr',
            'tt', 'u', 'ul', 'var', 'video',
        }
        self.singletags = {
            "area", "base", "br", "col", "command", "embed", "hr", "img",
            "input", "keygen", "link", "meta", "param", "source", "track",
            "wbr",
        }
        self.stack = []
        self.insvg = False
        super().__init__()

    def handle_starttag(self, starttag, attrs):
        if self.stack and self.stack[-1] == 'svg':
            return

        self.assertIn(starttag, self.pairtags | self.singletags, "unknown html tag")
        if starttag in self.pairtags:
            self.stack.append(starttag)

    def handle_startendtag(self, startendtag, attrs):
        if self.stack and self.stack[-1] == 'svg':
            return

        self.assertIn(startendtag, self.singletags)

    def handle_endtag(self, endtag):
        if self.stack[-1] == 'svg' and endtag != 'svg':
            return

        starttag = self.stack.pop()
        self.assertEqual(starttag, endtag, "malformatted html")


class TestController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Starting builtin server in a daemon thread")
        th = Thread(target=bottle.run, daemon=True, kwargs={
            "host": "localhost",
            "port": 8012,
            "debug": True
        })
        th.start()

        # Wait up to 2 second the server is ready
        for i in range(10):
            th.join(.2)
            try:
                urlreq.urlopen("http://localhost:8012/health")
            except ConnectionRefusedError:
                if i == 9:
                    raise
            else:
                break

    def setUp(self):
        self.html_sanitizer = HTMLSanitizer(self.assertEqual, self.assertIn)
        bottle.template = MagicMock()
        bottle.template.side_effect = bottle_template

    def tearDown(self):
        bottle.template = bottle_template

    def test_healthcheck(self):
        with urlreq.urlopen("http://localhost:8012/health") as res:
            self.assertEqual(res.status, 200)

    def test_get_new_form(self):
        with urlreq.urlopen("http://localhost:8012/") as res:
            bottle.template.assert_called_with('newform.html')
            self.assertEqual(res.status, 200)
            self.html_sanitizer.feed(res.read().decode())

    def test_get_html(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_lipsum
            with urlreq.urlopen("http://localhost:8012/lipsum") as res:
                bottle.template.assert_called_with(
                    'highlight', code=snippet_lipsum.code, language=config.DEFAULT_LANGUAGE)
                self.assertEqual(res.status, 200)
                self.html_sanitizer.feed(res.read().decode())

            MockSnippet.get_by_id.return_value = snippet_python
            with urlreq.urlopen("http://localhost:8012/egg.py") as res:
                bottle.template.assert_called_with(
                    'highlight', code=snippet_python.code, language='python')
                self.assertEqual(res.status, 200)
                self.html_sanitizer.feed(res.read().decode())

    def test_get_raw(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_lipsum
            with urlreq.urlopen("http://localhost:8012/raw/lipsum") as res:
                self.assertEqual(res.status, 200)
                self.assertEqual(res.read().decode(), snippet_lipsum.code)

            MockSnippet.get_by_id.return_value = snippet_python
            with urlreq.urlopen("http://localhost:8012/raw/egg.py") as res:
                self.assertEqual(res.status, 200)
                self.assertEqual(res.read().decode(), snippet_python.code)
