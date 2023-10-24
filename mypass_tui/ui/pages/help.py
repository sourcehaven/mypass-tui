from textual.app import ComposeResult
from textual.widgets import Label, Static

from mypass_tui.localization import i18n

HELP_PAGE_ID = "help_page"


class HelpPage(Static):
    def compose(self) -> ComposeResult:
        yield Label(i18n.help, classes="title")
