languages = [
    ('c', 'c'),
    ('cpp', 'cpp'),
    ('cs', 'csharp'),
    ('css', 'css'),
    ('diff', 'diff'),
    ('go', 'go'),
    ('h', 'objectivec'),
    ('html', 'html'),
    ('ini', 'ini'),
    ('java', 'java'),
    ('js', 'javascript'),
    ('json', 'json'),
    ('kts', 'kotlin'),
    ('less', 'less'),
    ('lua', 'lua'),
    ('md', 'md'),  # markdown
    ('py', 'python'),
    ('rb', 'ruby'),
    ('rs', 'rust'),
    ('sass', 'sass'),
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
    lang_or_ext = (lang_or_ext or '').casefold()
    if lang_or_ext in exttolang:
        return lang_or_ext
    return langtoext.get(lang_or_ext)


def parse_language(lang_or_ext):
    lang_or_ext = (lang_or_ext or '').casefold()
    if lang_or_ext in langtoext:
        return lang_or_ext
    return exttolang.get(lang_or_ext)
