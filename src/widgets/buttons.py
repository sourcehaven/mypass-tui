from typing import Callable

from textual import on
from textual.app import ComposeResult
from textual.widgets import Static, Button

HELP_PAGE_ID = "help_page"
HELP_PAGE_TITLE = "Help"

GAP_SIZE = 15


class ButtonPair(Static):
    DEFAULT_CSS = """
    ButtonPair {
        layout: horizontal;
    }
    
    #left_button {
        margin: 2 2 0 2;
        width: 50%;
    }
    
    #right_button {
        margin: 2 2 0 2;
        width: 50%;
    }
    """

    def __init__(
        self,
        left_callback: Callable[[Button.Pressed], None],
        right_callback: Callable[[Button.Pressed], None],
        left_text: str = "Submit",
        right_text: str = "Cancel",
    ):
        super().__init__()
        self.left_callback = left_callback
        self.right_callback = right_callback

        self.left_text = left_text
        self.right_text = right_text

    def compose(self) -> ComposeResult:
        yield Button(self.left_text, variant="primary", id="left_button")
        yield Button(self.right_text, variant="error", id="right_button")

    @on(Button.Pressed, "#left_button")
    async def on_left_pressed(self, pressed: Button.Pressed):
        self.left_callback(pressed)

    @on(Button.Pressed, "#right_button")
    async def on_right_pressed(self, pressed: Button.Pressed):
        self.right_callback(pressed)
