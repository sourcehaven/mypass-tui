from textual.app import ComposeResult

from .dialog import DialogScreen
from ..pages import HelpPage


class HelpScreen(DialogScreen):

    def _compose(self) -> ComposeResult:
        yield HelpPage()
