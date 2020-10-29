root = __import__('pathlib').Path(__file__).resolve().parent
__import__('bottle').TEMPLATE_PATH = [str(root / 'views')]

languages_exts = {
    'py': 'python',
    'js': 'javascript',
    'md': 'markdown',
    'cs': 'csharp',
    'sh': 'kotlin',
    'h': 'objectivec',
    'hpp': 'cpp',
    'rb': 'ruby',
    'rs': 'rust',
    'ts': 'typescript',
    'yml': 'yaml',
    'txt': 'plaintext',
    'html': 'html',
    'css': 'css',
    None: '',
}
