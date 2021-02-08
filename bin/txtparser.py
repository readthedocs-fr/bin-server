class TxtParser:
    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def parse(content):
        parsed = list()
        for line in content.splitlines():
            if line.startswith('#'):
                continue
            parsed.append(line)
        return parsed

    def parse_file(self):
        with open(self.filename, 'r') as file:
            return TxtParser.parse(file.read())
