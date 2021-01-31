import bottle as bt
from pathlib import Path
from metrics import Time
from bin import root, config, models
from bin.highlight import highlight, parse_language, parse_extension, languages


@bt.route('/health', method='GET')
def healthcheck():
    return "alive"


@bt.route('/', method='GET')
def get_new_form():
    parentid = bt.request.query.parentid
    lang = bt.request.query.lang or config.DEFAULT_LANGUAGE
    code = models.Snippet.get_by_id(parentid).code if parentid else ""
    return bt.template(
        'newform.html',
        languages=languages,
        default_language=lang,
        code=code,
        parentid=parentid,
    )


@bt.route('/assets/<filepath:path>')
def assets(filepath):
    return bt.static_file(filepath, root=root.joinpath('assets'))


@bt.route('/new', method='POST')
def post_new():
    content_length = bt.request.get_header('Content-Length')
    if content_length is None:
        raise bt.HTTPError(411, "Content-Length required")
    if int(content_length) > config.MAXSIZE:
        raise bt.HTTPError(413, f"Payload too large, we accept maximum {config.MAXSIZE}")

    files = bt.request.files
    forms = bt.request.forms

    code = None
    ext = parse_extension(config.DEFAULT_LANGUAGE)
    maxusage = config.DEFAULT_MAXUSAGE
    lifetime = config.DEFAULT_LIFETIME
    parentid = ''

    try:
        if files:
            part = next(files.values())
            code = part.file.read(config.MAXSIZE)
            ext = parse_extension(Path(part.filename).suffix.lstrip('.')) or ext
        if forms:
            code = forms.get('code', '').encode('utf-8') or code
            ext = parse_extension(forms.get('lang')) or ext
            maxusage = int(forms.get('maxusage') or maxusage)
            lifetime = Time(forms.get('lifetime') or lifetime)
            parentid = forms.get('parentid', '')

        if not code:
            raise ValueError("Code is missing")
        if maxusage < 0:
            raise ValueError("Maximum usage must be positive")
        if lifetime < 0:
            raise ValueError("Lifetime must be positive")
        if parentid:
            try:
                models.Snippet.get_by_id(parentid)
            except KeyError:
                raise ValueError("Parent does not exist")
    except ValueError as exc:
        raise bt.HTTPError(400, str(exc))

    snippet = models.Snippet.create(code, maxusage, lifetime, parentid)
    bt.redirect(f'/{snippet.id}.{ext}')


@bt.route('/<snippetid>', method='GET')
@bt.route('/<snippetid>.<ext>', method='GET')
def get_html(snippetid, ext=None):
    try:
        snippet = models.Snippet.get_by_id(snippetid)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")
    lang = parse_language(ext) or config.DEFAULT_LANGUAGE
    codehl = highlight(snippet.code, lang)
    return bt.template(
        'highlight.html',
        codehl=codehl,
        lang=lang,
        ext=ext,
        snippetid=snippetid,
        parentid=snippet.parentid,
    )


@bt.route('/raw/<snippetid>', method='GET')
@bt.route('/raw/<snippetid>.<ext>', method='GET')
def get_raw(snippetid, ext=None):
    try:
        snippet = models.Snippet.get_by_id(snippetid)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")

    bt.response.headers['Content-Type'] = 'text/plain'
    return snippet.code
