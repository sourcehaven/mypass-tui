from textual.widgets import Input

prompt_text = ">"


class InputPrompt(Input):
    def __init__(self):
        super().__init__(placeholder=prompt_text)
