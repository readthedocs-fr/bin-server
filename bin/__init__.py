root = __import__("pathlib").Path(__file__).resolve().parent
__import__('bottle').TEMPLATE_PATH = [str(root / 'views')]
languageOfExtension = {
    'py': 'python',
    'js': 'javascript',
    'md': 'markdown',
    'cs': 'csharp',
    'sh': 'shell',
    'kts': 'kotlin',
    'h': 'objectivec',
    'hpp': 'cpp',
    'rb': 'ruby',
    'rs': 'rust',
    'ts': 'typescript',
    'yml': 'yaml',
    'txt': 'plaintext',
    None: "",
}
