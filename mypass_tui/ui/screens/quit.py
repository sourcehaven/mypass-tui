from textual.widgets import Button, Label

from mypass_tui.globals import i18n
from mypass_tui.localization import KEY_BUTTON, KEY_TITLE, KEY_SUBTITLE
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

    def __init__(self, title=i18n[KEY_TITLE]["quit"], subtitle=i18n[KEY_SUBTITLE]["confirm_quit"]):
        self.subtitle = subtitle
        super().__init__(
            title,
            submit_btn_text=i18n[KEY_BUTTON]["yes"],
            cancel_btn_text=i18n[KEY_BUTTON]["no"],
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
