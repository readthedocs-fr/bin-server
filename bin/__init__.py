root = __import__("pathlib").Path(__file__).resolve().parent
__import__('bottle').TEMPLATE_PATH = [str(root / 'views')]
