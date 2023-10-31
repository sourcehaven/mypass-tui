from textual.widgets import Button

from mypass_tui.globals import i18n
from mypass_tui.localization import KEY_TITLE, KEY_SUBTITLE
from mypass_tui.ui.screens import QuitScreen
from mypass_tui.ui.util.session import restart_app


class RestartScreen(QuitScreen):

    def __init__(self, title=i18n[KEY_TITLE]["restart"], subtitle=i18n[KEY_SUBTITLE]["confirm_restart"]):
        super().__init__(
            title=title,
            subtitle=subtitle,
        )

    def on_submit_pressed(self, _: Button.Pressed):
        restart_app(self.app)
