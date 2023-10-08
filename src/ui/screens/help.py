from textual.app import ComposeResult

from .secondary import SecondaryScreen
from ..pages import HelpPage


class HelpScreen(SecondaryScreen):
    def _compose(self) -> ComposeResult:
        yield HelpPage()
