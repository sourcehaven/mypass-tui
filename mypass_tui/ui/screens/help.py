from mypass_tui.localization import KEY_TITLE
from mypass_tui.ui.screens import SecondaryScreen

from textual.app import ComposeResult
from textual.widgets import Label, Static

from mypass_tui.globals import i18n

HELP_PAGE_ID = "help_page"


class HelpPage(Static):
    def compose(self) -> ComposeResult:
        yield Label(i18n[KEY_TITLE]["help"], classes="title")


class HelpScreen(SecondaryScreen):
    def _compose(self) -> ComposeResult:
        yield HelpPage()
