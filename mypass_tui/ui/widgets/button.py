from typing import Awaitable, Callable, Union

from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, Static

from mypass_tui.utils.asynchronous import await_me_maybe


class ButtonPair(Static):
    DEFAULT_CSS = """
    ButtonPair {
        dock: bottom;
        layout: horizontal;
    }
    
    #left_button {
        content-align: center middle;
        margin-top: 1;
        margin-right: 2;
        width: 50%;
    }
    
    #right_button {
        content-align: center middle;
        margin-top: 1;
        margin-left: 2;
        width: 50%;
    }
    """

    def __init__(
        self,
        left_callback: Callable[[Button.Pressed], Union[None, Awaitable[None]]],
        right_callback: Callable[[Button.Pressed], Union[None, Awaitable[None]]],
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
        return await await_me_maybe(self.left_callback, pressed)

    @on(Button.Pressed, "#right_button")
    async def on_right_pressed(self, pressed: Button.Pressed):
        return await await_me_maybe(self.right_callback, pressed)
