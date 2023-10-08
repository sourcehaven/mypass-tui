from typing import ClassVar

import pyperclip
from textual.binding import BindingType, Binding
from textual.widgets import Input

from src.settings import bindings


class EpicInput(Input):

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding(bindings["cut"], "cut", show=False),
        Binding(bindings["copy"], "copy", show=False),
        Binding(bindings["paste"], "paste", show=False),
    ]

    DEFAULT_CSS = """
    Input {
        background: $boost;
        color: $text;
        padding: 0 2;
        border: tall $background;
        width: 100%;
        height: 1;
        min-height: 1;
    }
    Input:focus {
        border: tall $accent !important;
    }
    Input:hover {
        border: tall $accent 20%;
    }
    Input>.input--cursor {
        background: $surface;
        color: $text;
        text-style: reverse;
    }
    Input>.input--placeholder, Input>.input--suggestion {
        color: $text-disabled;
    }
    Input.-invalid {
        border: tall $error 60%;
    }
    Input.-invalid:focus{
        border: tall $error !important;
    }
    Input.-invalid:hover {
        border: tall $error 80%;
    }
    """

    def action_cut(self):
        pyperclip.copy(self.value)
        self.value = ""

    def action_copy(self):
        pyperclip.copy(self.value)

    def action_paste(self):
        self.value = pyperclip.paste()
        self.cursor_position = len(self.value)
