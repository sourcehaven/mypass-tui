from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Label, Static, Button

from src.widgets.buttons import ButtonPair
from src.widgets.labeled_input import LabeledInput

HELP_PAGE_ID = "help_page"
HELP_PAGE_TITLE = "Help"

GAP_SIZE = 15


class SignUpPage(Static):
    def compose(self) -> ComposeResult:
        yield Label("Sign Up", classes="title")

        with ScrollableContainer():
            yield LabeledInput("Username", GAP_SIZE, required=True)
            yield LabeledInput("Password", GAP_SIZE)
            yield LabeledInput("First name", GAP_SIZE)
            yield LabeledInput("Last name", GAP_SIZE)
            yield LabeledInput("Email", GAP_SIZE)
        yield ButtonPair(
            left_callback=self.on_submit_pressed,
            right_callback=self.on_cancel_pressed,
        )

    def on_submit_pressed(self, _: Button.Pressed):
        pass

    def on_cancel_pressed(self, _: Button.Pressed):
        self.screen.dismiss()
