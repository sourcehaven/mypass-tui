from typing import Iterable, Callable

from rich.text import Text
from textual.binding import Binding
from textual.suggester import Suggester
from textual.validation import Validator
from textual.widgets import Input
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import ProgressBar, Label, Static

from .epic_input import EpicInput

import mypass_tui.model.password as mpw
from mypass_tui.settings import bindings, settings
from ...localization import i18n

SHOW = "Show"
HIDE = "Hide"


class PasswordStrengthBar(ProgressBar):
    DEFAULT_CSS = """
    PasswordStrengthBar {
        margin-left: 17;
    }
    """

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(
            total=len(mpw.PasswordStrength) - 1,
            show_eta=False,
            show_percentage=False,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def update_progress(self, progress: int, /):
        self.update(progress=progress)


class PasswordStrengthLabel(Label):
    DEFAULT_CSS = """
    PasswordStrengthLabel {
        margin-left: 1;
    }
    """
    pass


class PasswordStrength(Static):

    DEFAULT_CSS = """
    Horizontal {
        height: 1;
    }
    """

    strength_function: Callable[[str], mpw.PasswordStrength] = mpw.default_get_password_strength

    def compose(self) -> ComposeResult:
        self.bar = PasswordStrengthBar()
        self.label = PasswordStrengthLabel()
        horizontal = Horizontal(
            self.bar,
            self.label,
        )
        horizontal.styles.height = 1
        yield horizontal

    def update_strength(self, password: str):
        strength = PasswordStrength.strength_function(password)
        self.bar.update(progress=strength.value)
        self.label.update(str(strength))


class Password(EpicInput):

    BINDINGS = [
        Binding(bindings["password_visibility"], "show_hide", show=False)
    ]

    def _set_hint(self, show=True):
        index = 0 if show else 1
        self.border_subtitle = i18n.subtitle__show_hide_password[index]
        """
        self.border_subtitle = (
            f"Press [bold]{bindings['password_visibility']}[/bold] "
            f"to [bold][italic]{'show' if show else 'hide'}[/italic][/bold] password"
        )
        """

    def __init__(
        self,
        value: str = None,
        placeholder: str = "",
        password: bool = True,
        strength_bar: PasswordStrength = None,
        *,
        suggester: Suggester | None = None,
        validators: Validator | Iterable[Validator] | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        editable: bool = True,
    ):
        super().__init__(
            value=value,
            placeholder=placeholder,
            password=password,
            suggester=suggester,
            validators=validators,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            editable=editable,
        )
        self.password_mask = settings["password_mask"]
        self.strength_bar = strength_bar
        self._set_hint(show=True)

    def action_show_hide(self):
        self.password = not self.password
        self._set_hint(self.password)

    def on_input_changed(self, changed_input: Input.Changed):
        if self.strength_bar:
            self.strength_bar.update_strength(changed_input.value)
