from textual.widgets import Button, Label

from mypass_tui.localization import i18n
from mypass_tui.ui.screens import DialogScreen


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

    def __init__(self, title=i18n.title__exit, subtitle=i18n.subtitle__confirm_quit):
        self.subtitle = subtitle
        super().__init__(
            title,
            submit_btn_text=i18n.button__yes,
            cancel_btn_text=i18n.button__no,
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
