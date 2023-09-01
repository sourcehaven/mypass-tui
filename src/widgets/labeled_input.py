from textual.widgets import Label, Static, Input

from src.util.field_label import format_field_text


class LabeledInput(Static):

    DEFAULT_CSS = """
    LabeledInput {
        layout: horizontal;
    }
    
    .input_label {
        margin-top: 1;
        width: auto;
        content-align: left middle;
    }
    
    .labeled_input {
        align: left middle;
        width: 90%;
    }
    """

    def __init__(
            self,
            text: str,
            length: int = "auto",
            required=False,
            id: str | None = None,
            classes: str | None = None,
            name: str | None = None,
    ):
        super().__init__(id=id, classes=classes, name=name)
        self.text = text

        if isinstance(length, int):
            self.length = length
        else:
            self.length = len(text) + 4

        self.required = required

    def compose(self):
        text = format_field_text(self.text, length=self.length, required=self.required)
        yield Label(text, classes="input_label")
        yield Input(classes="labeled_input")
