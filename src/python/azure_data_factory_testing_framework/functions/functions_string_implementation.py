def concat(arguments: list) -> str:
    return "".join(arguments)


def trim(text: str, trim_argument: str) -> str:
    return text.strip(trim_argument[0])


def replace(input_str: str, pattern: str, replacement: str) -> str:
    return input_str.replace(pattern, replacement)


def split(input_str: str, delimiter: str) -> list:
    return input_str.split(delimiter)
