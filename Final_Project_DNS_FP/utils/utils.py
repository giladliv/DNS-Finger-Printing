FORMAT_TIME = "%m/%d/%Y %H:%M:%S"
JSON_FILE_NAME_DEFAULT = ''

def get_lines_from_file(file_name: str):
    with open(file_name, 'r') as f:
        return [s.replace('\n', '') for s in f.readlines()]

def replace_whitespace(input_string, replacement=' '):
    return replacement.join(input_string.split())


