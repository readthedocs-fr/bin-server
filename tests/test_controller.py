import bottle
import re
import signal
import unittest
import urllib.request as urlreq
from bin import config
from bin.models import Snippet
from bottle import template as bottle_template
from html.parser import HTMLParser
from textwrap import dedent
from threading import Thread
from unittest.mock import patch, MagicMock


snippet_lipsum = Snippet(ident='lipsum', code="Lipsum", views_left=float('+inf'))
snippet_python = Snippet(ident='egg', code='print("Hello world")', views_left=float('+inf'))
snippet_htmlxss = Snippet(ident='htmlxss', code=dedent("""\
    <DOCTYPE html>
    <html>
        <head>
            <script>alert("XSS");</script>
        </head>
    </html>'"""), views_left=float('+inf'))


class HTMLSanitizer(HTMLParser):
    def __init__(self, testcase):
        self.testcase = testcase
        self.pairtags = {
            'a', 'abbr', 'acronym', 'address', 'applet', 'article', 'aside',
            'audio', 'b', 'basefont', 'bdi', 'bdo', 'big', 'blockquote',
            'body', 'button', 'canvas', 'caption', 'center', 'cite', 'code',
            'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn',
            'dialog', 'dir', 'div', 'dl', 'doctype', 'dt', 'em', 'fieldset',
            'figcaption', 'figure', 'font', 'footer', 'form', 'frame',
            'frameset', 'head', 'header', 'hgroup', 'h1', 'h2', 'h3', 'h4',
            'h5', 'h6', 'html', 'i', 'iframe', 'ins', 'kbd', 'label', 'legend',
            'li', 'main', 'map', 'mark', 'menu', 'menuitem', 'meter', 'nav',
            'noframes', 'noscript', 'object', 'ol', 'output', 'p', 'picture',
            'pre', 'progress','q', 'rp', 'rt', 'ruby', 's', 'samp', 'script',
            'section', 'select', 'small', 'span', 'strike', 'strong', 'style',
            'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template',
            'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'tt',
            'u', 'ul', 'var', 'video',
        }
        self.singletags = {
            'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img',
            'input', 'keygen', 'link', 'meta', 'param', 'source', 'track',
            'wbr',
        }
        self.stack = []
        self.insvg = False
        super().__init__()

    def handle_starttag(self, starttag, attrs):
        if self.stack and self.stack[-1] == 'svg':
            return

        if starttag in ('option', 'optgroup'):
            # <option> and <optgroup> can be single or pair, no need to verify
            # append them the the stack, we just verify their immediate parent
            # tag is a <select> or a <datalist>.
            self.testcase.assertTrue(self.stack[-1] in ('select', 'datalist'),
                "%s must be direct child of select or datalist")
            return

        self.testcase.assertIn(starttag, self.pairtags | self.singletags, "unknown html tag")
        if starttag in self.pairtags:
            self.stack.append(starttag)

    def handle_startendtag(self, startendtag, attrs):
        if self.stack and self.stack[-1] == 'svg':
            return

        if startendtag in ('option', 'optgroup'):
            # <option> and <optgroup> can be single or pair, we just verify
            # their immediate parent tag is a <select> or a <datalist>.
            self.testcase.assertTrue(self.stack[-1] in ('select', 'datalist'),
                "%s must be direct child of select or datalist")
            return

        self.testcase.assertIn(startendtag, self.singletags)

    def handle_endtag(self, endtag):
        if self.stack[-1] == 'svg' and endtag != 'svg':
            return

        if endtag in ('option', 'optgroup'):
            # <option> and <optgroup> can be single or pair, they were not
            # added to the stack, we just verify their immediate parent is
            # a <select> or a <datalist>
            self.testcase.assertTrue(self.stack[-1] in ('select', 'datalist'),
                "%s must be direct child of select or datalist")
            return

        starttag = self.stack.pop()
        self.testcase.assertEqual(starttag, endtag, "malformatted html")


class HTMLPreCodeMatcher(HTMLSanitizer):
    def __init__(self, testcase, automaton):
        self.automaton = automaton
        self.matched = False
        super().__init__(testcase)

    def handle_data(self, data):
        if self.automaton.match(data):
            self.matched = True
            self.testcase.assertIn('table', self.stack)
            tablei = self.stack.index('table')
            self.testcase.assertEqual(self.stack[tablei + 1], 'tbody', "code must be enclosed in <table><tbody>")

    def feed(self, data):
        super().feed(data)
        self.testcase.assertTrue(self.matched, "not found")


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

        # Wait up to 2 second for the server to boot
        for i in range(10):
            th.join(.2)
            try:
                urlreq.urlopen("http://localhost:8012/health")
            except ConnectionRefusedError:
                if i == 9:
                    raise
            else:
                break

        bottle.template = MagicMock()
        bottle.template.side_effect = bottle_template

    @classmethod
    def tearDownClass(cls):
        bottle.template = bottle_template

    def setUp(self):
        self.html_sanitizer = HTMLSanitizer(self)
        bottle.template.reset_mock()

    # =====

    def test_healthcheck(self):
        with urlreq.urlopen("http://localhost:8012/health") as res:
            self.assertEqual(res.status, 200)

    def test_get_new_form(self):
        with urlreq.urlopen("http://localhost:8012/") as res:
            self.assertTrue(bottle.template.called)
            self.assertEqual(bottle.template.call_args.args, ('newform.html',))
            self.assertEqual(res.status, 200)
            self.html_sanitizer.feed(res.read().decode())

    def test_get_html(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_lipsum
            with urlreq.urlopen("http://localhost:8012/lipsum") as res:
                self.assertTrue(bottle.template.called)
                self.assertEqual(bottle.template.call_args.args, ('highlight.html',))
                self.assertEqual(res.status, 200)
                self.html_sanitizer.feed(res.read().decode())

            bottle.template.reset_mock()
            MockSnippet.get_by_id.return_value = snippet_python
            with urlreq.urlopen("http://localhost:8012/egg.py") as res:
                self.assertTrue(bottle.template.called)
                self.assertEqual(bottle.template.call_args.args, ('highlight.html',))
                self.assertEqual(res.status, 200)
                self.html_sanitizer.feed(res.read().decode())

    def test_get_raw(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_lipsum
            with urlreq.urlopen("http://localhost:8012/raw/lipsum") as res:
                bottle.template.assert_not_called()
                self.assertEqual(res.status, 200)
                self.assertEqual(res.read().decode(), snippet_lipsum.code)

            MockSnippet.get_by_id.return_value = snippet_python
            with urlreq.urlopen("http://localhost:8012/raw/egg.py") as res:
                bottle.template.assert_not_called()
                self.assertEqual(res.status, 200)
                self.assertEqual(res.read().decode(), snippet_python.code)

    def test_against_xss(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_htmlxss
            with urlreq.urlopen("http://localhost:8012/htmlxss") as res:
                self.assertEqual(res.status, 200)
                matcher = HTMLPreCodeMatcher(self, re.compile('.*alert.*', re.S))
                matcher.feed(res.read().decode())

            with urlreq.urlopen("http://localhost:8012/raw/htmlxss") as res:
                self.assertEqual(res.status, 200)
                self.assertIn('Content-Type', res.headers)
                mimetype = res.headers['Content-Type'].partition(';')[0]
                self.assertEqual(mimetype, 'text/plain')
