from textual.app import ComposeResult

from .secondary import SecondaryScreen
from ..pages import AboutPage


class AboutScreen(SecondaryScreen):
    def _compose(self) -> ComposeResult:
        yield AboutPage()
