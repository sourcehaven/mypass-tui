from textual.app import ComposeResult
from textual.widgets import Label, TabPane

HELP_TAB_ID = "help_tab"
HELP_TAB_TITLE = "Help"


class HelpTabPane(TabPane):

    def compose(self) -> ComposeResult:
        yield Label("Help", classes="title")
