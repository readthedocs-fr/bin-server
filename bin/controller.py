import bottle as bt
from pathlib import Path
from bin import root, config
from bin.models import Snippet
from bin.utils import parse_language, parse_extension
import contextlib


@bt.route('/', method='GET')
def get_new_form():
    return bt.template('newform.html')


@bt.route('/assets/<filepath:path>')
def assets(filepath):
    return bt.static_file(filepath, root=root.joinpath('assets'))


@bt.route('/new', method='POST')
def post_new():
    content_length = bt.request.get_header('Content-Length')
    if content_length is None:
        raise bt.HTTPError(411, "Content-Length required")
    if int(content_length) > config.SNIPPET_MAX_SIZE:
        raise bt.HTTPError(413, f"Payload too large, we accept maximum {config.SNIPPET_MAX_SIZE} bytes")

    files = bt.request.files
    forms = bt.request.forms

    # Default values
    code = None
    ext = config.SNIPPET_DEAULT_EXTENSION
    lang = 'plaintext'
    maxusage = config.DEFAULT_SNIPPET_MAX_USAGE

    # Extract from multi-part file
    if files:
        part = next(files.values())
        with contextlib.suppress(ValueError):
            ext = parse_extension(Path(part.filename).suffix[1:])
        code = part.file.read(config.SNIPPET_MAX_SIZE)

    # Extract from multi-part form or x-www-form-urlencoded
    if forms:
        with contextlib.suppress(ValueError, KeyError):
            ext = parse_extension(forms['lang'])
        with contextlib.suppress(KeyError):
            code = forms['code'].encode('latin-1')
        with contextlib.suppress(ValueError):
            maxusage = int(forms['maxusage'])

    if not code:
        raise bt.HTTPError(417, "Missing code")

    snippet = Snippet.create(code.decode('utf-8'), maxusage)
    bt.redirect(f'/{snippet.id}.{ext}')


@bt.route('/<snippet_id>', method='GET')
@bt.route('/<snippet_id>.<ext>', method='GET')
def get_html(snippet_id, ext=None):
    try:
        snippet = Snippet.get_by_id(snippet_id)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")
    language = parse_language(ext)
    return bt.template('highlight', code=snippet.code, language=language)


@bt.route('/raw/<snippet_id>', method='GET')
@bt.route('/raw/<snippet_id>.<ext>', method='GET')
def get_raw(snippet_id, ext=None):
    try:
        snippet = Snippet.get_by_id(snippet_id)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")
    return snippet.code
