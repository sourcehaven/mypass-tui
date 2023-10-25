from textual.app import ComposeResult
from textual.widgets import Static

from mypass_tui import session
from mypass_tui.ui.widgets import VaultTree

FOLDER_PAGE_ID = "folder_page"


class FolderPage(Static):
    def compose(self) -> ComposeResult:
        self.folder_widget = VaultTree(session.user.vault_entries)
        yield self.folder_widget