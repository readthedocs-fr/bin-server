import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


class OlLiHtmlFormatter(HtmlFormatter):
    def __init__(self, **options):
        super().__init__(**options)
        if options.get('linenos', False) == 'ol':
            self.linenos = 3
            self.lineseparator = '</li><!--\n--><li>'

    def wrap(self, source, outfile):
        if self.linenos == 3:
            source = self._wrap_olli(source)
        return super().wrap(source, outfile)

    def _wrap_olli(self, inner):
        yield 0, '<ol><li>'
        yield from inner
        yield 0, '</li></ol>'


_html_formatter = OlLiHtmlFormatter(wrapcode=True, linenos='ol', style='monokai')


def highlight(code, language):
    lexer = get_lexer_by_name(language)
    return pygments.highlight(code, lexer, _html_formatter)
