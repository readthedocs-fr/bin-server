import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


class TableHtmlFormatter(HtmlFormatter):
    def __init__(self, **options):
        super().__init__(**options)
        if options.get('linenos', False) == 'bin-table':
            self.linenos = 3

    def wrap(self, source, outfile):
        if self.linenos == 3:
            source = self._wrap_table(source)
        yield from source

    def _wrap_table(self, inner):
        yield 0, '<table class="highlight"><tbody>'
        for i, (t, l) in enumerate([*inner, (1, '')]):
            yield t, f'<tr><td class="line-number" id=L{i + 1} value={i + 1}></td><td class="line-content">{l}</td></tr>\n'
        yield 0, '</tbody></table>'


_html_formatter = TableHtmlFormatter(linenos='bin-table', style='monokai')


def highlight(code, language):
    lexer = get_lexer_by_name(language)
    return pygments.highlight(code, lexer, _html_formatter)
