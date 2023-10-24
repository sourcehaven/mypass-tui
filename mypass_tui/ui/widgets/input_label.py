from textual.app import ComposeResult
from textual.containers import Container
from textual.dom import DOMNode
from textual.widget import Widget
from textual.widgets import Input, Label, Static, Switch, TextArea

REQUIRED_TEXT = " [red]*[/red]"


class InputLabel(Label):
    DEFAULT_CSS = """
    InputLabel {
        height: 100%;
        align: center middle;
    }
    """

    def __init__(self, text: str, required: bool = False, length: int = 16):
        super().__init__()
        self.required = required
        self.text = format_field_text(text, length=length, required=required)

    def compose(self):
        yield Label(self.text)


class LabeledInput(Static):
    def __init__(self, label: InputLabel, input: Input | TextArea, *widgets: Widget):
        super().__init__()
        self.label = label
        self.input = input
        self.widgets = widgets

    @property
    def is_valid(self):
        return not self.label.required or (self.label.required and bool(self.value))

    def compose(self) -> ComposeResult:
        yield Container(
            self.label,
            self.input,
            *self.widgets,
            classes="labeled_input_container",
        )

    @property
    def value(self):
        import mypass_tui.ui.widgets.password as wpw

        if isinstance(self.input, wpw.Password):
            import mypass_tui.model.password as mpw

            return mpw.Password(self.input.value, hide=self.input.password)
        if isinstance(self.input, Input):
            return self.input.value
        if isinstance(self.input, TextArea):
            return self.input.text
        if isinstance(self.input, Switch):
            return self.input.value

        raise ValueError("Must be an instance of Input or TextArea")

    def has_input(self):
        return bool(self.value)


def get_invalid_fields(node: DOMNode):
    labeled_inputs = node.query(LabeledInput)
    return [
        labeled_input.label.text.replace(REQUIRED_TEXT, "").strip()
        for labeled_input in labeled_inputs
        if not labeled_input.is_valid
    ]


def format_field_text(text: str, length: int, required=False):
    if required:
        text += REQUIRED_TEXT
        length += len(REQUIRED_TEXT) - 2

    return f"{text:<{length}}"
