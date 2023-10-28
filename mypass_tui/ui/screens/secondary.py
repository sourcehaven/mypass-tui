from abc import abstractmethod

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label

from mypass_tui.globals import i18n, bindings
from mypass_tui.ui.widgets import ButtonPair


class SecondaryScreen(ModalScreen):
    BINDINGS = [
        Binding(bindings["pop_screen"], "pop_screen", "Quit", show=False),
    ]

    DEFAULT_CSS = """
    #secondary {
        padding: 1 4;
        height: 84%;
        width: 92%;
        background: $surface;
        color: $text;
        border: tall $background;
    }
    """

    @abstractmethod
    def _compose(self):
        pass

    def compose(self) -> ComposeResult:
        yield Container(*self._compose(), id="secondary")

    def action_pop_screen(self):
        self.dismiss(None)


class DialogScreen(SecondaryScreen):
    def __init__(
        self,
        title: str,
        submit_btn_text: str = i18n["button"]["submit"],
        cancel_btn_text: str = i18n["button"]["cancel"],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.title_label = Label(title, classes="title")
        self.submit_btn_text = submit_btn_text
        self.cancel_btn_text = cancel_btn_text

    @property
    def screen_title(self):
        return self.title_label.renderable

    @screen_title.setter
    def screen_title(self, title: str):
        self.title_label.renderable = title
        self.title_label.refresh()

    @abstractmethod
    def _compose(self):
        pass

    def compose(self) -> ComposeResult:
        yield Container(
            self.title_label,
            *self._compose(),
            ButtonPair(
                left_callback=self.on_submit_pressed,
                right_callback=self.on_cancel_pressed,
                left_text=self.submit_btn_text,
                right_text=self.cancel_btn_text,
            ),
            id="secondary",
        )

    @abstractmethod
    def on_submit_pressed(self, _: Button.Pressed):
        pass

    def on_cancel_pressed(self, _: Button.Pressed) -> None:
        self.dismiss()
