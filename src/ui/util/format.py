
def snake_case_text_to_sentence(text: str):
    words = text.split('_')
    words[0] = words[0].capitalize()
    return " ".join(words)
