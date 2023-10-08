from textual.widgets import Input

prompt_text = ">"


class InputPrompt(Input):
    def __init__(self, id: str | None = None):
        super().__init__(id=id, placeholder=prompt_text)
