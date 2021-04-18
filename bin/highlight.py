""" HTML highlighted code export and language tools """


import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


languages = [
    # (ext, lang)
    ('c', 'c'),
    ('cpp', 'cpp'),
    ('cs', 'csharp'),
    ('css', 'css'),
    ('diff', 'diff'),
    ('erl', 'erlang'),
    ('ex', 'elixir'),
    ('go', 'go'),
    ('h', 'objectivec'),
    ('hs', 'haskell'),
    ('html', 'html'),
    ('ini', 'ini'),
    ('java', 'java'),
    ('js', 'javascript'),
    ('json', 'json'),
    ('kt', 'kotlin'),
    ('less', 'less'),
    ('lisp', 'lisp'),
    ('lua', 'lua'),
    ('md', 'markdown'),
    ('php', 'php'),
    ('pl', 'perl'),
    ('py', 'python'),
    ('rb', 'ruby'),
    ('rs', 'rust'),
    ('sass', 'sass'),
    ('scala', 'scala'),
    ('scss', 'scss'),
    ('sh', 'bash'),
    ('sql', 'sql'),
    ('swift', 'swift'),
    ('toml', 'toml'),
    ('ts', 'typescript'),
    ('txt', 'text'),
    ('xml', 'xml'),
    ('yml', 'yaml'),
]
exttolang = {ext: lang for ext, lang in languages}
langtoext = {lang: ext for ext, lang in languages}


def parse_extension(ext):
    """ From a language extension, get a language """
    ext = (ext or '').casefold()
    if ext in langtoext:
        return ext  # this is a lang already
    return exttolang.get(ext)


def parse_language(lang):
    """ From a language name, get an extension """
    lang = (lang or '').casefold()
    if lang in exttolang:
        return lang  # this is an ext already
    return langtoext.get(lang)



class _TableHtmlFormatter(HtmlFormatter):
    """
    Extension to the default pygment HtmlFormatter to control the html
    skeleton output, class names and line numbering.
    """
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


_html_formatter = _TableHtmlFormatter(linenos='bin-table', style='monokai')


def highlight(code, language):
    """ Pretty html export of ``code`` using syntax highlighting """
    lexer = get_lexer_by_name(language, startinline=True)
    return pygments.highlight(code, lexer, _html_formatter)
