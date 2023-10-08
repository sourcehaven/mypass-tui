from itertools import cycle
from typing import Iterable, Literal

import pyperclip
from rich.text import Text
from textual.binding import Binding
from textual.coordinate import Coordinate
from textual.events import Key
from textual.widgets import DataTable

from .input_prompt import InputPrompt
from ..screens.input import InputScreen
from ...model.vault_entry import VaultEntry
from ...model.password import Password
from ...settings import bindings


cursors = cycle(["row", "column", "cell"])


class VaultTable(DataTable):
    COLUMNS = ["Username", "Password", "Title", "Website", "Folder", "Notes", "Tags"]
    REQUIRED = [True, True, False, False, False, False, False]

    BINDINGS = [
        Binding(bindings["select"], "select_cursor", "Select", show=False),
        Binding(bindings["copy"], "clipboard_copy", "Copy to clipboard", show=False),
        Binding(bindings["table_mode"], "table_mode"),
        Binding(bindings["password_visibility"], "select_cursor", "Select", show=False),
    ]

    def __init__(
            self,
            *,
            show_header: bool = True,
            show_row_labels: bool = True,
            fixed_rows: int = 0,
            fixed_columns: int = 0,
            zebra_stripes: bool = False,
            header_height: int = 1,
            show_cursor: bool = True,
            cursor_foreground_priority: Literal["renderable", "css"] = "css",
            cursor_background_priority: Literal["renderable", "css"] = "renderable",
            cursor_type: Literal["cell", "row", "column", "none"] = "cell",
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            disabled: bool = False,
            vault_entries: Iterable[VaultEntry],
    ):
        super().__init__(
            show_header=show_header, show_row_labels=show_row_labels, fixed_rows=fixed_rows,
            fixed_columns=fixed_columns, zebra_stripes=zebra_stripes, header_height=header_height,
            show_cursor=show_cursor, cursor_foreground_priority=cursor_foreground_priority,
            cursor_background_priority=cursor_background_priority, cursor_type=cursor_type,
            name=name, id=id, classes=classes, disabled=disabled
        )

        self.row_counter = 1
        self.vault_entries = vault_entries

        for column in self.COLUMNS:
            self.add_column(column, key=column)

        for entry in vault_entries:
            self.add_row(*entry.row, key=entry.id)

    def update_cells(self, new_values: dict):
        if new_values:
            for key, val in new_values.items():
                self.update_cell_at(
                    coordinate=Coordinate(row=self.cursor_row, column=self.COLUMNS.index(key)),
                    value=val,
                    update_width=True
                )

    def on_key(self, key: Key):
        if key.name == bindings["select"]:
            inputs: list[tuple[str, str, bool]] = []
            if self.cursor_type == "cell":
                value = self.get_cell_at(self.cursor_coordinate)
                inputs = [(self.COLUMNS[self.cursor_column], value, self.REQUIRED[self.cursor_column])]

            elif self.cursor_type == "row":
                values = self.get_row_at(self.cursor_row)
                inputs = list(zip(self.COLUMNS, values, self.REQUIRED))

            if inputs:
                self.app.push_screen(
                    InputScreen(title="Edit", inputs=inputs),
                    callback=self.update_cells,
                )

    def add_entries(self, *entries: VaultEntry):
        for entry in entries:
            self.add_row(*entry.values, label=Text(str(self.row_counter)))
            self.row_counter += 1

    def set_prompt(self, text):
        prompt: InputPrompt = self.screen.query_one("#table_prompt")
        prompt.placeholder = text

    def action_clipboard_copy(self) -> None:
        def get_value():
            if self.cursor_type == "cell":
                value = self.get_cell_at(self.cursor_coordinate)
                self.set_prompt(
                    f"{VaultTable.COLUMNS[self.cursor_coordinate.column]} in row {self.cursor_coordinate.row+1} copied to clipboard"
                )
                return value.data if isinstance(value, Password) else value
            if self.cursor_type == "row":
                self.set_prompt(f"Row {self.cursor_row} copied to clipboard")
                return ",".join(str(e) for e in self.get_row_at(self.cursor_row))

        value = get_value()
        pyperclip.copy(str(value))

    def action_table_mode(self):
        table = self.screen.query_one(DataTable)
        current_cursor = next(cursors)
        table.cursor_type = current_cursor
        self.set_prompt(f"Cursor mode: {current_cursor}")

    def on_data_table_cell_selected(self, cell: DataTable.CellSelected):
        if isinstance(cell.value, Password):
            cell.value.toggle()
            self.update_cell_at(self.cursor_coordinate, value=cell.value, update_width=True)

    def on_data_table_cell_highlighted(self, highlighted: DataTable.CellHighlighted):
        help = f'Press {bindings["copy"]} to copy highlighted value to clipboard'
        if highlighted.coordinate.column == self.COLUMNS.index("Password"):
            help += f' or {bindings["password_visibility"]} to show/hide password'
        self.set_prompt(help)

    def on_data_table_column_selected(self, column_selected: DataTable.ColumnSelected):
        self.remove_column(column_selected.column_key)
        self.add_column()
