from textual.widgets import Button, Label

from .secondary import DialogScreen
from ... import session


class QuitScreen(DialogScreen):
    DEFAULT_CSS = """
    #secondary {
        padding: 1 4;
        height: 14;
        width: 60;
        background: $surface;
        color: $text;
        border: tall $background;
    }
    """

    def __init__(self, title="Exit app", subtitle="Are you sure you want to exit?"):
        self.subtitle = subtitle
        super().__init__(
            title,
            submit_btn_text="Yes",
            cancel_btn_text="No",
        )

    def _compose(self):
        lbl = Label(self.subtitle)
        lbl.styles.height = "1fr"
        lbl.styles.width = "1fr"
        lbl.styles.content_align = "center", "middle"
        yield lbl

    def on_submit_pressed(self, _: Button.Pressed):
        self.dismiss(True)

    def on_cancel_pressed(self, _: Button.Pressed) -> None:
        self.dismiss(False)
