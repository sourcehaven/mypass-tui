from textual.app import ComposeResult
from textual.widgets import Button, Input, Label

from .dialog import DialogScreen
from ..widgets.buttons import ButtonPair
from ..widgets.labeled_input import LabeledInput


class PasswordDialog(DialogScreen):

    def __init__(self, title: str, password_label: str, name: str | None = None, id: str | None = None, classes: str | None = None):
        super().__init__(name=name, id=id, classes=classes)
        self.title = title
        self.password_label = password_label

    def _compose(self) -> ComposeResult:
        yield Label(self.title, classes="title")
        yield LabeledInput(self.password_label, required=True)
        yield ButtonPair(
            left_callback=self.on_submit_pressed,
            right_callback=self.on_cancel_pressed,
        )

    def on_submit_pressed(self, _: Button.Pressed) -> None:
        self.dismiss(self.query_one(Input).value)

    def on_cancel_pressed(self, _: Button.Pressed) -> None:
        self.dismiss(None)

    def on_input_submitted(self, submitted_input: Input.Submitted):
        self.dismiss(submitted_input.value)
