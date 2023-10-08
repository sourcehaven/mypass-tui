from textual.app import ComposeResult
from textual.widgets import Button, Input

from .secondary import DialogScreen
from ..widgets import Password, InputLabel, LabeledInput
from ...settings import settings


class PasswordDialog(DialogScreen):
    def __init__(
        self,
        title: str,
        password_label: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(title=title, name=name, id=id, classes=classes)
        self.password_label = password_label

    def _compose(self) -> ComposeResult:
        yield LabeledInput(
            InputLabel(self.password_label, required=True),
            Password(id="password", password_mask=settings["password_mask"]),
        )

    def on_submit_pressed(self, _: Button.Pressed) -> None:
        self.dismiss(self.query_one(Input).value)

    def on_input_submitted(self, submitted_input: Input.Submitted):
        self.dismiss(submitted_input.value)