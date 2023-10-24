from typing import ClassVar, Iterable, Literal

import pyperclip
from rich.highlighter import Highlighter
from textual.binding import Binding, BindingType
from textual.suggester import Suggester
from textual.validation import Validator
from textual.widgets import Input

from mypass_tui.settings import bindings
from mypass_tui.ui.widgets import Feedback


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

    def __init__(
        self,
        value: str | None = None,
        placeholder: str = "",
        highlighter: Highlighter | None = None,
        password: bool = False,
        *,
        suggester: Suggester | None = None,
        validators: Validator | Iterable[Validator] | None = None,
        validate_on: Iterable[Literal["blur", "changed", "submitted"]] | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(
            value=value,
            placeholder=placeholder,
            highlighter=highlighter,
            password=password,
            suggester=suggester,
            validators=validators,
            validate_on=validate_on,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def action_cut(self):
        pyperclip.copy(self.value)
        self.value = ""

        Feedback.info(self.screen, f"{self.id.title()} cut to clipboard")

    def action_copy(self):
        pyperclip.copy(self.value)
        Feedback.info(self.screen, f"{self.id.title()} copied to clipboard")

    def action_paste(self):
        self.value = pyperclip.paste()
        self.cursor_position = len(self.value)
