from itertools import cycle

from textual.app import ComposeResult
from textual.widgets import DataTable, Static

from ..widgets.input_prompt import InputPrompt
from ..widgets.vault_table import VaultTable, populate

TABLE_PAGE_ID = "table_view_page"
TABLE_PAGE_TITLE = "Table view"


cursors = cycle(["column", "row", "cell"])


class TableViewPage(Static):
    def compose(self) -> ComposeResult:
        table = VaultTable()
        populate(table)
        yield table
        yield InputPrompt()

    def key_c(self):
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)
