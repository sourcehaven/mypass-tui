import pyperclip
from textual.widgets import Button, Label

from mypass_tui.globals import i18n
from mypass_tui.localization import KEY_FEEDBACK, KEY_BUTTON, KEY_TITLE
from mypass_tui.model import FeedbackStyle
from mypass_tui.ui.screens import DialogScreen
from mypass_tui.ui.widgets import Feedback


class TokenScreen(DialogScreen):
    def __init__(self, token: str):
        super().__init__(
            title=i18n[KEY_TITLE]["token"],
            submit_btn_text=i18n[KEY_BUTTON]["copy_token"],
            cancel_btn_text=i18n[KEY_BUTTON]["close"],
        )
        self.token = token
        pyperclip.copy(token)

    def _compose(self):
        yield Label(i18n["registration_token"], classes="header")
        yield Label(self.token, classes="multiline")
        feedback = Feedback(i18n[KEY_FEEDBACK]["info"]["token_copy"], classes="multiline")
        feedback.set_style(style=FeedbackStyle.INFO)
        feedback.offset = (0, -4)
        yield feedback

    def on_submit_pressed(self, _: Button.Pressed):
        pyperclip.copy(self.token)
