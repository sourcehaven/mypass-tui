import pyperclip
from textual.widgets import Button, Label

from mypass_tui.ui.screens.secondary import DialogScreen
from mypass_tui.ui.widgets.feedback import Feedback, FeedbackStyle


class TokenScreen(DialogScreen):
    def __init__(self, token: str):
        super().__init__(
            title="Token",
            submit_btn_text="Copy token",
            cancel_btn_text="Close",
        )
        self.token = token
        pyperclip.copy(token)

    def _compose(self):
        yield Label("Registration token:", classes="header")
        yield Label(self.token, classes="multiline")
        feedback = Feedback(
            "Token copied to clipboard! "
            "Store your token securely as this is your only option "
            "to recover your vault if you forgot your master password",
            classes="multiline",
        )
        feedback.set_style(style=FeedbackStyle.INFO)
        feedback.offset = (0, -4)
        yield feedback

    def on_submit_pressed(self, _: Button.Pressed):
        pyperclip.copy(self.token)
