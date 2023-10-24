from textual.app import ComposeResult
from textual.widgets import Static, Input

from mypass_tui.ui.widgets.vault_tree import VaultTree
from mypass_tui import session

FOLDER_PAGE_ID = "folder_page"


class FolderPage(Static):

    def compose(self) -> ComposeResult:
        self.folder_widget = VaultTree(session.user.vault_entries)
        self.input_prompt = Input(id="tree_prompt")

        yield self.folder_widget
        yield self.input_prompt
