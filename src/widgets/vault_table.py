import pyperclip
from textual.widgets import DataTable


def populate(table: DataTable) -> DataTable:
    table.add_columns("Row", "Title", "Username", "Website")
    for row in range(100):
        table.add_row(*[str(row), *[str(n) for n in range(3)]])
    return table


class VaultTable(DataTable):
    def on_data_table_cell_selected(self, cell: DataTable.CellSelected):
        # Exact value
        pyperclip.copy(cell.value)

    def on_data_table_row_selected(self, row: DataTable.RowSelected):
        # Selected row number
        pyperclip.copy(str(self.get_row_at(row.cursor_row)))

    def on_data_table_column_selected(self, column: DataTable.ColumnSelected):
        # Selected column number
        pyperclip.copy(str(list(self.get_column_at(column.cursor_column))))
