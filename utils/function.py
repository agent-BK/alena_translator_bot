def read_text(file_path):
    with open(file_path, 'r', encoding="utf-8") as text:
        return text.read()


def get_help_text():
    return read_text("data/help.txt")


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
