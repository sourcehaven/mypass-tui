from textual.events import Focus, Blur
from textual.widgets import Input


class InputPrompt(Input):
    def __init__(self, id: str | None = None, prompt_text: str = "> "):
        self.hint_text = ""
        super().__init__(id=id, placeholder=prompt_text)

    def on_focus(self, focus: Focus):
        self.value = self.prompt_text

    def on_blur(self, blur: Blur):
        self.value = ''
        self.placeholder = self.hint_text
