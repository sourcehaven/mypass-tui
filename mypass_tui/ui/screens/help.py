from textual.app import ComposeResult

from mypass_tui.ui.pages import HelpPage
from mypass_tui.ui.screens.secondary import SecondaryScreen


class HelpScreen(SecondaryScreen):
    def _compose(self) -> ComposeResult:
        yield HelpPage()
