from textual.app import ComposeResult
from textual.widgets import Input, Static

from mypass_tui import session
from mypass_tui.ui.widgets.vault_table import VaultTable

TABLE_PAGE_ID = "table_page"


class TablePage(Static):
    def compose(self) -> ComposeResult:
        self.table = VaultTable(id="vault_table", zebra_stripes=True, vault_entries=session.user.vault_entries)
        yield self.table
