from textual.app import ComposeResult
from textual.widgets import Static

from ..widgets.input_prompt import InputPrompt
from ..widgets.vault_table import VaultTable
from ... import session

TABLE_PAGE_ID = "table_view_page"
TABLE_PAGE_TITLE = "Table view"


class TableViewPage(Static):
    def compose(self) -> ComposeResult:
        table = VaultTable(id="vault_table", zebra_stripes=True, vault_entries=session.user.vault_entries)
        yield table
        yield InputPrompt(id="table_prompt")
