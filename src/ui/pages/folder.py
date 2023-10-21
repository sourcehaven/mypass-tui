from textual.app import ComposeResult
from textual.widgets import Static, Input, Tree

from ..widgets.vault_tree import VaultTree
from ... import session
from ...model.vault_entry import append_tree, VaultEntry

FOLDER_PAGE_ID = "folder_view_page"
FOLDER_PAGE_TITLE = "Folder view"


class TreeViewPage(Static):

    def compose(self) -> ComposeResult:
        self.folder_widget = VaultTree(session.user.vault_entries)
        self.input_prompt = Input(id="tree_prompt")

        yield self.folder_widget
        yield self.input_prompt
