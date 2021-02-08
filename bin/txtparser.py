def parse(content):
    parsed = list()
    for line in content.splitlines():
        if line.startswith('#'):
            continue
        parsed.append(line)
    return parsed

def parse_file(filename):
    with open(filename, 'r') as file:
        return parse(file.read())
