from textual.app import ComposeResult

from .dialog import DialogScreen
from ..pages import AboutPage


class AboutScreen(DialogScreen):

    DEFAULT_CSS = """
    #dialog {
        max-width: 100;
        max-height: 25;
    }
    """

    def _compose(self) -> ComposeResult:
        yield AboutPage()
