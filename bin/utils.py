languages = [
    ('txt', 'plaintext'),
    ('sh', 'bash'),
    ('c', 'c'),
    ('cs', 'csharp'),
    ('hpp', 'cpp'),
    ('css', 'css'),
    ('diff', 'diff'),
    ('go', 'go'),
    ('html', 'html'),
    ('ini', 'ini'),
    ('java', 'java'),
    ('js', 'javascript'),
    ('json', 'json'),
    ('kts', 'kotlin'),
    ('less', 'less'),
    ('lua', 'lua'),
    ('md', 'markdown'),
    ('h', 'objectivec'),
    ('py', 'python'),
    ('rb', 'ruby'),
    ('rs', 'rust'),
    ('scss', 'sass'),
    ('sql', 'sql'),
    ('swift', 'swift'),
    ('toml', 'toml'),
    ('ts', 'typescript'),
    ('xml', 'xml'),
    ('yml', 'yaml'),
]
exttolang = {ext: language for ext, language in languages}
langtoext = {language: ext for ext, language in languages}


def parse_extension(lang_or_ext):
    lang_or_ext = (lang_or_ext or '').casefold()
    if lang_or_ext in exttolang:
        return lang_or_ext
    return langtoext.get(lang_or_ext)


def parse_language(lang_or_ext):
    lang_or_ext = (lang_or_ext or '').casefold()
    if lang_or_ext in langtoext:
        return lang_or_ext
    return exttolang.get(lang_or_ext)
