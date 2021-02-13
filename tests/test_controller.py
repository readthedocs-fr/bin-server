import bottle
import html
import re
import unittest
import urllib.request as urlreq
import socket
from bin.models import Snippet
from bottle import template as bottle_template
from html.parser import HTMLParser
from textwrap import dedent
from threading import Thread
from unittest.mock import patch, MagicMock
from genpw import pronounceable_passwd as ppwd


def make_snippet(ident, code):
    return Snippet(ident=ident, code=code, views_left=float('+inf'), parentid='')

snippet_lipsum = make_snippet('lipsum', code="Lorem ipsum dolor sit amet")
snippet_python = make_snippet('egg', code='print("Hello world")')
snippet_htmlxss = make_snippet('htmlxss', code='<script>alert("XSS");</script>')
snippet_classified = make_snippet('classified', code='T_xJV3P^FcvYijzH')
snippet_utf8 = make_snippet('utf8', code='éèùÈÇ')

UA_HUMAN = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"
UA_BOT = "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)"

class FakeSnippet(Snippet):
    snippets = {}
    last_snippet = None

    @classmethod
    def create(cls, code, maxusage, lifetime, parentid):
        ident = ppwd(6)
        snippet = cls(ident, code, maxusage, parentid)
        cls.snippets[ident] = cls.last_snippet = snippet
        return snippet

    @classmethod
    def get_by_id(cls, ident):
        snippet = cls.snippets[ident]
        snippet.view_left -= 1
        if snippet.view_left == 0:
            del cls.snippets[snippet]
        return snippet

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
            'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script',
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
            bottle.template.assert_called_once()
            self.assertEqual(res.status, 200)
            self.html_sanitizer.feed(res.read().decode())

    def test_get_html(self):
        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.get_by_id.return_value = snippet_lipsum
            with urlreq.urlopen("http://localhost:8012/lipsum") as res:
                bottle.template.assert_called_once()
                self.assertEqual(res.status, 200)
                self.html_sanitizer.feed(res.read().decode())

            bottle.template.reset_mock()
            MockSnippet.get_by_id.return_value = snippet_python
            with urlreq.urlopen("http://localhost:8012/egg.py") as res:
                bottle.template.assert_called_once()
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

    def test_unicode(self):
        russian_text = (
            "В колониальные времена территория, занятая ныне Ист-Виллиджем, "
            "была окраиной Нью-Йорка."
        )

        with patch('bin.models.Snippet') as MockSnippet:
            MockSnippet.create.side_effect = FakeSnippet.create
            MockSnippet.get_by_id.side_effeft = FakeSnippet.get_by_id

            with self.subTest(agent='curl/7.64.0'):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('127.0.0.1', 8012))
                # $ curl localhost:8012 -X POST -d "code=В колониальные..."
                sock.send(dedent(b"""\
                    POST /new HTTP/1.1
                    Host: localhost:8012
                    User-Agent: curl/7.64.0
                    Accept: */*
                    Content-Length: 165
                    Content-Type: application/x-www-form-urlencoded

                    code=\xd0\x92 \xd0\xba\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xbd\xd0\xb8\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb5 \xd0\xb2\xd1\x80\xd0\xb5\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xb0 \xd1\x82\xd0\xb5\xd1\x80\xd1\x80\xd0\xb8\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd1\x8f, \xd0\xb7\xd0\xb0\xd0\xbd\xd1\x8f\xd1\x82\xd0\xb0\xd1\x8f \xd0\xbd\xd1\x8b\xd0\xbd\xd0\xb5 \xd0\x98\xd1\x81\xd1\x82-\xd0\x92\xd0\xb8\xd0\xbb\xd0\xbb\xd0\xb8\xd0\xb4\xd0\xb6\xd0\xb5\xd0\xbc, \xd0\xb1\xd1\x8b\xd0\xbb\xd0\xb0 \xd0\xbe\xd0\xba\xd1\x80\xd0\xb0\xd0\xb8\xd0\xbd\xd0\xbe\xd0\xb9 \xd0\x9d\xd1\x8c\xd1\x8e-\xd0\x99\xd0\xbe\xd1\x80\xd0\xba\xd0\xb0.""".decode('latin-1')).encode('latin-1'))

                resp = sock.recv(1024)
                sock.close()
                self.assertEqual(resp.partition(b"\r\n")[0], b"HTTP/1.0 303 See Other")
                self.assertEqual(FakeSnippet.last_snippet.code, russian_text.encode('utf-8'))

            with self.subTest(agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('127.0.0.1', 8012))
                sock.send(dedent(b"""\
                    POST /new HTTP/1.1
                    Host: localhost:8012
                    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0
                    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
                    Accept-Language: en-US,fr;q=0.8,fr-FR;q=0.5,en;q=0.3
                    Accept-Encoding: gzip, deflate
                    Content-Type: application/x-www-form-urlencoded
                    Content-Length: 500
                    Origin: http://localhost:8012
                    DNT: 1
                    Connection: keep-alive
                    Referer: http://localhost:8012/
                    Upgrade-Insecure-Requests: 1
                    Sec-GPC: 1

                    code=%D0%92+%D0%BA%D0%BE%D0%BB%D0%BE%D0%BD%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B0+%D1%82%D0%B5%D1%80%D1%80%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D1%8F%2C+%D0%B7%D0%B0%D0%BD%D1%8F%D1%82%D0%B0%D1%8F+%D0%BD%D1%8B%D0%BD%D0%B5+%D0%98%D1%81%D1%82-%D0%92%D0%B8%D0%BB%D0%BB%D0%B8%D0%B4%D0%B6%D0%B5%D0%BC%2C+%D0%B1%D1%8B%D0%BB%D0%B0+%D0%BE%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%BE%D0%B9+%D0%9D%D1%8C%D1%8E-%D0%99%D0%BE%D1%80%D0%BA%D0%B0.&parentid=&maxusage=&lifetime=&lang=txt""".decode('latin-1')).encode('latin-1'))

                resp = sock.recv(1024)
                sock.close()
                self.assertEqual(resp.partition(b"\r\n")[0], b"HTTP/1.0 303 See Other")
                self.assertEqual(FakeSnippet.last_snippet.code, russian_text.encode('utf-8'))
