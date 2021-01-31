""" HTML highlighted code export and language tools """


import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


languages = [
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
    ('md', 'md'),  # markdown
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
exttolang = {ext: language for ext, language in languages}
langtoext = {language: ext for ext, language in languages}


def parse_extension(lang_or_ext):
    """ From a language name or a language extension, get a language """
    lang_or_ext = (lang_or_ext or '').casefold()
    if lang_or_ext in exttolang:
        return lang_or_ext
    return langtoext.get(lang_or_ext)


def parse_language(lang_or_ext):
    """ From a language name or a language extension, get an extension """
    lang_or_ext = (lang_or_ext or '').casefold()
    if lang_or_ext in langtoext:
        return lang_or_ext
    return exttolang.get(lang_or_ext)



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
    lexer = get_lexer_by_name(language)
    return pygments.highlight(code, lexer, _html_formatter)
