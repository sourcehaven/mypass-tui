from textual.app import ComposeResult

from src.pages.signup import SignUpPage
from src.screens.dialog import DialogScreen


class SignUpScreen(DialogScreen):

    def _compose(self) -> ComposeResult:
        yield SignUpPage()
