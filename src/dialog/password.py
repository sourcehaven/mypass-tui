from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Input, Label


class PasswordDialog(Screen):

    def __init__(self, title: str, name: str | None = None, id: str | None = None, classes: str | None = None):
        super().__init__(name=name, id=id, classes=classes)
        self.title = title

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.title, classes="password_label"),
            Input(password=True, classes="password_prompt"),
            Button("Submit", variant="primary", id="btn_submit"),
            Button("Cancel", variant="error", id="btn_cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_submit":
            self.dismiss(self.query_one(Input).value)
        else:
            self.dismiss(None)

    def on_input_submitted(self, submitted_input: Input.Submitted):
        self.dismiss(submitted_input.value)
