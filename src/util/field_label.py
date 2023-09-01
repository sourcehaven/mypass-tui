
def format_field_text(text: str, length: int, required=False):
    if required:
        postfix = ' [red]*[/red]'
        text += postfix
        length += len(postfix) - 2

    return f"{text:<{length}}"
