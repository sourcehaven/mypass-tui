from textual.app import ComposeResult

from mypass_tui.ui.pages import AboutPage
from mypass_tui.ui.secondary import SecondaryScreen


class AboutScreen(SecondaryScreen):
    def _compose(self) -> ComposeResult:
        yield AboutPage()
