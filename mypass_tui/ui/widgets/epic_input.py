from typing import ClassVar, Iterable, Literal

import pyperclip
from rich.console import RenderableType
from rich.highlighter import Highlighter
from textual.binding import Binding, BindingType
from textual.suggester import Suggester
from textual.validation import Validator
from textual.widgets import Input

from mypass_tui.globals import i18n, bindings
from mypass_tui.localization import fill_placeholders, KEY_LABEL, KEY_FEEDBACK
from mypass_tui.ui.util.query import query_active_tab
from mypass_tui.ui.widgets import Feedback


class EpicInput(Input):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding(bindings["cut"], "cut", show=False),
        Binding(bindings["copy"], "copy", show=False),
        Binding(bindings["paste"], "paste", show=False),
    ]

    DEFAULT_CSS = """
    EpicInput:focus {
        border: tall $accent !important;
    }
    EpicInput:hover {
        border: tall $accent 40%;
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
        Feedback.info(
            query_active_tab(self.screen),
            fill_placeholders(i18n[KEY_FEEDBACK]["info"]["cut"], i18n[KEY_LABEL][self.id])
        )

    def action_copy(self):
        pyperclip.copy(self.value)
        Feedback.info(
            query_active_tab(self.screen),
            fill_placeholders(i18n[KEY_FEEDBACK]["info"]["copy"], i18n[KEY_LABEL][self.id])
        )

    def action_paste(self):
        self.value = pyperclip.paste()
        self.cursor_position = len(self.value)
