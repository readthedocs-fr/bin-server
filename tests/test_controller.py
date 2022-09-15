import bottle
import unittest
import urllib.request as urlreq

from bottle import template as bottle_template
from html.parser import HTMLParser
from threading import Thread
from unittest.mock import patch, MagicMock
from urllib.parse import urlencode
from urllib.error import HTTPError

import bin as binmod
from bin.models import Snippet
from .fake_config import FakeConfig
from .html_sanitizer import HTMLSanitizer


def make_snippet(ident, code):
    return Snippet(ident=ident, code=code, views_left=float('+inf'), parentid='', token=None)

snippet_lipsum = make_snippet('lipsum', code="Lorem ipsum dolor sit amet")
snippet_python = make_snippet('egg', code='print("Hello world")')
snippet_htmlxss = make_snippet('htmlxss', code='<script>alert("XSS");</script>')
snippet_classified = make_snippet('classified', code='T_xJV3P^FcvYijzH')
snippet_brainfuck = make_snippet('brainfuck', code='++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++++.+++++++++.')

UA_HUMAN = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"
UA_BOT = "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)"


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

        # Wait up to 5 seconds for the server to boot
        for i in range(10):
            th.join(.5)
            try:
                urlreq.urlopen("http://localhost:8012/health")
            except ConnectionRefusedError:
                if i == 9:
                    raise
            else:
                break

        cls.config = FakeConfig()
        patch_config = patch.object(binmod.controller, 'config', cls.config)
        patch_config.start()
        cls.addClassCleanup(patch_config.stop)

        mock_bt_tmpl = MagicMock()
        mock_bt_tmpl.side_effect = bottle.template
        patch_bt_tmpl = patch.object(bottle, 'template', mock_bt_tmpl)
        patch_bt_tmpl.start()
        cls.addClassCleanup(patch_bt_tmpl.stop)

    def setUp(self):
        self.html_sanitizer = HTMLSanitizer(self)
        bottle.template.reset_mock()
        self.config.clear()

    # =====

    def test_healthcheck(self):
        with urlreq.urlopen("http://localhost:8012/health") as res:
            self.assertEqual(res.status, 200)

    def test_get_new_form(self):
        with urlreq.urlopen("http://localhost:8012/") as res:
            bottle.template.assert_called_once()
            self.assertEqual(res.status, 200)
            self.html_sanitizer.feed(res.read().decode())

    def test_missing_parentid(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.side_effect = KeyError('Snippet not found')
            with self.assertRaises(HTTPError) as exc:
                urlreq.urlopen("http://localhost:8012/?parentid=foo")

            self.assertEqual(exc.exception.code, 404)

    def test_get_html(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_lipsum
            with urlreq.urlopen("http://localhost:8012/lipsum") as res:
                bottle.template.assert_called_once()
                MockSnippet.get_by_id.assert_called_with(snippet_lipsum.id)
                self.assertEqual(res.status, 200)
                self.html_sanitizer.feed(res.read().decode())

            bottle.template.reset_mock()
            MockSnippet.get_by_id.return_value = snippet_python
            with urlreq.urlopen("http://localhost:8012/egg.py") as res:
                bottle.template.assert_called_once()
                MockSnippet.get_by_id.assert_called_with(snippet_python.id)
                self.assertEqual(res.status, 200)
                self.html_sanitizer.feed(res.read().decode())

    def test_get_raw(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_lipsum
            with urlreq.urlopen("http://localhost:8012/raw/lipsum") as res:
                bottle.template.assert_not_called()
                MockSnippet.get_by_id.assert_called_with(snippet_lipsum.id)
                self.assertEqual(res.status, 200)
                self.assertEqual(res.read().decode(), snippet_lipsum.code)


            MockSnippet.get_by_id.return_value = snippet_python
            with urlreq.urlopen("http://localhost:8012/raw/egg.py") as res:
                bottle.template.assert_not_called()
                MockSnippet.get_by_id.assert_called_with(snippet_python.id)
                self.assertEqual(res.status, 200)
                self.assertEqual(res.read().decode(), snippet_python.code)

    def test_get_wrong_extension(self):
        with patch('bin.models.Snippet') as MockSnippet, \
             patch('bin.controller.highlight') as MockHighlight:  # from-imported
            MockSnippet.get_by_id.return_value = snippet_lipsum
            MockHighlight.return_value = ''

            with urlreq.urlopen("http://localhost:8012/lipsum.idontexist") as res:
                self.assertEqual(res.status, 200)

            MockSnippet.get_by_id.assert_called_with(snippet_lipsum.id)
            MockHighlight.assert_called_with(snippet_lipsum.code, 'text')

    def test_get_hidden_extension(self):
        with patch('bin.models.Snippet') as MockSnippet, \
             patch('pygments.highlight') as MockHighlight:
            MockSnippet.get_by_id.return_value = snippet_brainfuck
            MockHighlight.return_value = ''

            with urlreq.urlopen("http://localhost:8012/brainfuck.bf") as res:
                self.assertEqual(res.status, 200)

            MockSnippet.get_by_id.assert_called_with(snippet_brainfuck.id)
            MockHighlight.assert_called_once()
            self.assertEqual(MockHighlight.call_args[0][0], snippet_brainfuck.code)
            self.assertIn('BrainfuckLexer', str(MockHighlight.call_args[0][1]))

    def test_against_xss(self):
        testcase = self

        class HTMLParserXSS(HTMLParser):
            def feed(self, data):
                self.found = False
                super().feed(data)
                testcase.assertTrue(self.found)

            def handle_data(self, data):
                if "XSS" in data:
                    self.found = True
                    # ``data`` is unescaped by the calling method already
                    testcase.assertEqual(data.strip(), snippet_htmlxss.code.strip())

        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_htmlxss
            with urlreq.urlopen("http://localhost:8012/htmlxss") as res:
                self.assertEqual(res.status, 200)
                HTMLParserXSS().feed(res.read().decode())

            with urlreq.urlopen("http://localhost:8012/raw/htmlxss") as res:
                self.assertEqual(res.status, 200)
                self.assertIn('Content-Type', res.headers)
                mimetype = res.headers['Content-Type'].partition(';')[0]
                self.assertEqual(mimetype, 'text/plain')

    def test_discordbot(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_classified

            req = urlreq.Request(
                "http://localhost:8012/raw/classified",
                headers={'User-Agent': UA_BOT},
            )
            with urlreq.urlopen(req) as res:
                MockSnippet.get_by_id.assert_not_called()
                self.assertEqual(res.status, 200)

            req = urlreq.Request(
                "http://localhost:8012/raw/classified",
                headers={'User-Agent': UA_HUMAN},
            )
            with urlreq.urlopen(req) as res:
                MockSnippet.get_by_id.assert_called()
                self.assertEqual(res.status, 200)

    def test_new_form(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.create.return_value = snippet_lipsum
            MockSnippet.get_by_id.return_value = snippet_lipsum

            data = urlencode({'code': snippet_lipsum.code}).encode()
            req = urlreq.Request(
                'http://localhost:8012/new',
                data=data,
                headers={
                    'Content-Length': str(len(data))
                }
            )

            with urlreq.urlopen(req) as res:
                MockSnippet.create.assert_called_with(
                    snippet_lipsum.code,
                    self.config.DEFAULT_MAXUSAGE,
                    self.config.DEFAULT_LIFETIME,
                    '',  # parentid
                    None,  # token
                )
                self.assertEqual(res.url, 'http://localhost:8012/lipsum.txt')
