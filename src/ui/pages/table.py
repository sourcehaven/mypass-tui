from textual.app import ComposeResult
from textual.widgets import Static, Input

from ..widgets.vault_table import VaultTable
from ... import session

TABLE_PAGE_ID = "table_view_page"
TABLE_PAGE_TITLE = "Table view"


class TableViewPage(Static):

    def compose(self) -> ComposeResult:
        self.table = VaultTable(id="vault_table", zebra_stripes=True, vault_entries=session.user.vault_entries)
        self.input_prompt = Input(id="table_prompt")

        yield self.table
        yield self.input_prompt
