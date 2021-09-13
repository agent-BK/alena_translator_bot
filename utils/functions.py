def read_text(file_path):
    with open(file_path, 'r', encoding="utf-8") as text:
        return text.read()


def get_help_text():
    return read_text("data/help.txt")


def get_key_dictionary(dictionary, search_value):
    for keys, values in dictionary.items():
        if values == search_value:
            return keys
