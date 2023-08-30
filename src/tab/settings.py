from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label, TabPane

from ..widgets import LabeledSwitch
from .about import ABOUT_TAB_TITLE
from .help import HELP_TAB_TITLE
from .new import NEW_TAB_TITLE
from .table import TABLE_TAB_TITLE
from .tree import TREE_VIEW_TAB_TITLE

SETTINGS_TAB_ID = "settings_tab"
SETTINGS_TAB_TITLE = "Settings"

GAP_SIZE = 10

tab_titles = NEW_TAB_TITLE, TABLE_TAB_TITLE, TREE_VIEW_TAB_TITLE, HELP_TAB_TITLE, ABOUT_TAB_TITLE


class SettingsTabPane(TabPane):
    def compose(self) -> ComposeResult:
        yield Label("Settings", classes="title")

        with VerticalScroll():
            for title in tab_titles:
                yield LabeledSwitch(title, GAP_SIZE)
