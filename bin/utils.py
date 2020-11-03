languages = [
    ('py', 'python'),
    ('js', 'javascript'),
    ('md', 'markdown'),
    ('cs', 'csharp'),
    ('sh', 'shell'),
    ('kts', 'kotlin'),
    ('h', 'objectivec'),
    ('hpp', 'cpp'),
    ('rb', 'ruby'),
    ('rs', 'rust'),
    ('ts', 'typescript'),
    ('yml', 'yaml'),
    ('txt', 'plaintext'),
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
