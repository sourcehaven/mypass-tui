from textual.app import ComposeResult
from textual.widgets import Label, Static

HELP_PAGE_ID = "help_page"
HELP_PAGE_TITLE = "Help"


class HelpPage(Static):
    def compose(self) -> ComposeResult:
        yield Label("Help", classes="title")
