from functools import cached_property
from itertools import cycle
from typing import Iterable, Literal, Callable

import pyperclip
from textual.binding import Binding
from textual.widgets import DataTable
from textual.widgets._data_table import RowKey

from .input_prompt import InputPrompt
from ..screens.input import InputScreen
from ... import session
from ...model.input_info import InputInfo
from ...model.vault_entry import VaultEntry
from ...model.password import Password
from ...settings import bindings


cursors = cycle(["row", "column", "cell"])


def callback(row_key: RowKey):
    def wrapper1(func: Callable[[str, dict], None]):
        def wrapper2(fields: dict[str, str]):
            func(row_key.value, fields)
        return wrapper2
    return wrapper1


class VaultTable(DataTable):

    BINDINGS = [
        Binding(bindings["select"], "select_cursor", "Select", show=False),
        Binding(bindings["copy"], "clipboard_copy", "Copy to clipboard", show=False),
        Binding(bindings["table_mode"], "table_mode"),
        Binding(bindings["password_visibility"], "password_visibility", "Select", show=False),
    ]

    def __init__(
            self,
            vault_entries: Iterable[VaultEntry],
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
    ):
        super().__init__(
            show_header=show_header, show_row_labels=show_row_labels, fixed_rows=fixed_rows,
            fixed_columns=fixed_columns, zebra_stripes=zebra_stripes, header_height=header_height,
            show_cursor=show_cursor, cursor_foreground_priority=cursor_foreground_priority,
            cursor_background_priority=cursor_background_priority, cursor_type=cursor_type,
            name=name, id=id, classes=classes, disabled=disabled
        )

        for column in VaultEntry.FIELDS:
            self.add_column(column.capitalize(), key=column)

        self.row_counter = 1
        self.vault_entries = {}
        self.add_entries(*vault_entries)

    def add_entries(self, *vault_entries: VaultEntry):
        for entry in vault_entries:
            key = str(entry.id)
            self.add_row(
                *entry.row,
                key=key,
                label=str(self.row_counter)
            )
            self.vault_entries[key] = entry
            self.row_counter += 1

    def update_cells(self, id: str, fields: dict[str, str]):
        for column_key, cell_value in fields.items():
            self.update_cell(
                row_key=id,
                column_key=column_key,
                value=cell_value,
                update_width=True,
            )
        session.user.vault_update(id=id, fields=fields)

    def on_data_table_cell_selected(self, selected_cell: DataTable.CellSelected):
        row_key = selected_cell.cell_key.row_key
        column_key = selected_cell.cell_key.column_key

        inputs = [InputInfo(name=column_key.value, value=selected_cell.value, required=VaultEntry.REQUIRED[self.cursor_column])]

        self.app.push_screen(
            InputScreen(title="Edit", inputs=inputs),
            callback=callback(row_key)(self.update_cells),
        )

    def on_data_table_row_selected(self, selected_row: DataTable.RowSelected):
        row_key = selected_row.row_key

        values = self.get_row_at(selected_row.cursor_row)
        inputs = [
            InputInfo(name=col, value=val, required=req)
            for col, val, req in zip(VaultEntry.FIELDS, values, VaultEntry.REQUIRED)
        ]
        self.app.push_screen(
            InputScreen(title="Edit", inputs=inputs),
            callback=callback(row_key)(self.update_cells),
        )

    def prompt_text(self, text):
        prompt = self.screen.query_one("#table_prompt")
        prompt.placeholder = text

    def action_clipboard_copy(self) -> None:
        def get_value():
            if self.cursor_type == "cell":
                value = self.get_cell_at(self.cursor_coordinate)
                self.prompt_text(
                    f"{VaultEntry.FIELDS[self.cursor_coordinate.column].capitalize()} "
                    f"in row {self.cursor_coordinate.row+1} copied to clipboard"
                )
                return value.data if isinstance(value, Password) else value
            if self.cursor_type == "row":
                self.prompt_text(f"Row {self.cursor_row} copied to clipboard")
                return ",".join(str(e) for e in self.get_row_at(self.cursor_row))

        value = get_value()
        pyperclip.copy(str(value))

    def action_table_mode(self):
        table = self.screen.query_one(DataTable)
        current_cursor = next(cursors)
        table.cursor_type = current_cursor
        self.prompt_text(f"Cursor mode: {current_cursor}")

    def action_password_visibility(self):
        value = self.get_cell_at(self.cursor_coordinate)
        if isinstance(value, Password):
            value.toggle()

    # def on_data_table_cell_selected(self, cell: DataTable.CellSelected):
    #    if isinstance(cell.value, Password):
    #        cell.value.toggle()
    #        self.update_cell_at(self.cursor_coordinate, value=cell.value, update_width=True)

    def on_data_table_cell_highlighted(self, highlighted: DataTable.CellHighlighted):
        help = f'Press {bindings["copy"]} to copy highlighted value to clipboard'
        if highlighted.coordinate.column == VaultEntry.FIELDS.index("password"):
            help += f' or {bindings["password_visibility"]} to show/hide password'
        self.prompt_text(help)

    def on_data_table_column_selected(self, column_selected: DataTable.ColumnSelected):
        self.remove_column(column_selected.column_key)
        self.add_column()
