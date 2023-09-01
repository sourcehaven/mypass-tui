from abc import abstractmethod

from textual.app import ComposeResult
from textual.containers import Container
from textual.events import Key
from textual.screen import ModalScreen


class DialogScreen(ModalScreen):
    DEFAULT_CSS = """
    DialogScreen {
        align: center middle;
    }
    
    #dialog {
        padding: 1 5;
        height: 75%;
        width: 85%;
        background: $surface;
        color: $text;
        border: tall $background;
    }
    """

    def compose(self) -> ComposeResult:
        yield Container(*self._compose(), id="dialog")

    @abstractmethod
    def _compose(self):
        pass

    def on_key(self, key: Key):
        if key.name == "escape":
            self.dismiss(None)
