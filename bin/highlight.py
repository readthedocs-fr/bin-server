""" HTML highlighted code export and language tools """

import os.path
import pygments
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


# ==================================================================== #
#                     Supported langages database                      #
# ==================================================================== #

languages = [
    # (ext, lang)
    ('c', 'c'),
    ('cpp', 'cpp'),
    ('cs', 'csharp'),
    ('css', 'css'),
    ('dart', 'dart'),
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
    ('jl', 'julia'),
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

def _load_more_languages():
    """ Save more langs to the ``exttolang`` and ``langtoext`` maps """
    for name, aliases, globs, _mimetypes in get_all_lexers():
        if not globs:
           continue
        name = name.lower()
        for glob in globs:
            ext = os.path.splitext(glob)[1][1:]
            langtoext.setdefault(name, ext)
            exttolang.setdefault(ext, name)
        for alias in aliases:
            ext = langtoext[name]
            langtoext.setdefault(alias, ext)
            exttolang.setdefault(ext, alias)

_load_more_languages()
del _load_more_languages

# ==================================================================== #
#                 Plaintext to stylized HTML utilities                 #
# ==================================================================== #

class _TableHtmlFormatter(HtmlFormatter):
    """
    Extension to the default pygment HtmlFormatter to control the html
    skeleton output, class names and line numbering.
    """
    def __init__(self, **options):
        super().__init__(**options)
        if options.get('linenos', False) == 'bin-table':
            self.linenos = 3

    def wrap(self, source, outfile=None):
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
