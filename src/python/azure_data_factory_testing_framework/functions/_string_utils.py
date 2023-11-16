def _trim_one_char(text: str, character: str) -> str:
    if text.startswith(character):
        text = text[1:]
    if text.endswith(character):
        text = text[:-1]
    return text
