from html.parser import HTMLParser

pairtags = {
    'a', 'abbr', 'acronym', 'address', 'applet', 'article', 'aside', 'audio',
    'b', 'basefont', 'bdi', 'bdo', 'big', 'blockquote', 'body', 'button',
    'canvas', 'caption', 'center', 'cite', 'code', 'colgroup', 'data',
    'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl',
    'doctype', 'dt', 'em', 'fieldset', 'figcaption', 'figure', 'font', 'footer',
    'form', 'frame', 'frameset', 'head', 'header', 'hgroup', 'h1', 'h2', 'h3',
    'h4', 'h5', 'h6', 'html', 'i', 'iframe', 'ins', 'kbd', 'label', 'legend',
    'li', 'main', 'map', 'mark', 'menu', 'menuitem', 'meter', 'nav', 'noframes',
    'noscript', 'object', 'ol', 'output', 'p', 'picture', 'pre', 'progress',
    'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select',
    'small', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup',
    'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th',
    'thead', 'time', 'title', 'tr', 'tt', 'u', 'ul', 'var', 'video',
}
singletags = {
    'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input',
    'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr',
}


class HTMLSanitizer(HTMLParser):

    def __init__(self, testcase):
        self.testcase = testcase
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

        self.testcase.assertIn(starttag, pairtags | singletags, "unknown html tag")
        if starttag in pairtags:
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

        self.testcase.assertIn(startendtag, singletags)

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
