from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label, Static

from ..widgets.labeled_switch import LabeledSwitch
from .about import ABOUT_PAGE_TITLE
from .help import HELP_PAGE_TITLE
from .new import NEW_PAGE_TITLE
from .table import TABLE_PAGE_TITLE
from .tree import TREE_VIEW_PAGE_TITLE

SETTINGS_PAGE_ID = "settings_page"
SETTINGS_PAGE_TITLE = "Settings"

tab_titles = NEW_PAGE_TITLE, TABLE_PAGE_TITLE, TREE_VIEW_PAGE_TITLE, HELP_PAGE_TITLE, ABOUT_PAGE_TITLE


class SettingsPage(Static):
    def compose(self) -> ComposeResult:
        yield Label("Settings", classes="title")

        with VerticalScroll():
            for title in tab_titles:
                yield LabeledSwitch(title, 15)
