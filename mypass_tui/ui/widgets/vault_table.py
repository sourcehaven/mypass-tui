from collections import UserString
from itertools import cycle
from typing import Callable, Iterable, Literal

import pyperclip
from textual.binding import Binding
from textual.widgets import DataTable
from textual.widgets._data_table import RowKey

from mypass_tui import session
from mypass_tui.localization import i18n
from mypass_tui.model.input_info import InputInfo
from mypass_tui.model.password import Password
from mypass_tui.model.vault_entry import VaultEntry
from mypass_tui.settings import bindings
from mypass_tui.utils.string import to_string

cursors = cycle(["row", "column", "cell"])


def callback(row_key: RowKey):
    def wrapper1(func: Callable[[str, dict], None]):
        def wrapper2(fields: dict[str, str]):
            if fields:
                func(row_key.value, fields)

        return wrapper2

    return wrapper1


class VaultTable(DataTable):
    BINDINGS = [
        Binding(bindings["select"], "select_cursor", "Select", show=False),
        Binding(bindings["copy"], "clipboard_copy", "Copy to clipboard", show=False),
        Binding(bindings["table_mode"], "table_mode"),
        Binding(bindings["password_visibility"], "password_visibility", "Show/hide password", show=False),
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
            show_header=show_header,
            show_row_labels=show_row_labels,
            fixed_rows=fixed_rows,
            fixed_columns=fixed_columns,
            zebra_stripes=zebra_stripes,
            header_height=header_height,
            show_cursor=show_cursor,
            cursor_foreground_priority=cursor_foreground_priority,
            cursor_background_priority=cursor_background_priority,
            cursor_type=cursor_type,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

        for label, column_key in zip(VaultEntry.TRANSLATED_FIELDS, VaultEntry.API_FIELDS):
            self.add_column(label=label, key=column_key)

        self.row_counter = 1
        self.vault_entries = {}
        self.add_entries(*vault_entries)

    @property
    def column_labels(self):
        return tuple(key.label.plain for key in self.columns.values())

    @property
    def column_keys(self):
        return tuple(key.value for key in self.columns.keys())

    def add_entries(self, *vault_entries: VaultEntry):
        for entry in vault_entries:
            key = str(entry.id)
            self.add_row(*entry.row, key=key, label=str(self.row_counter))
            self.vault_entries[key] = entry
            self.row_counter += 1

    def update_cells(self, id: str, fields: dict[str, str | UserString]):
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

        inputs = [
            InputInfo(
                name=column_key.value, value=selected_cell.value, required=VaultEntry.REQUIRED[self.cursor_column]
            )
        ]
        inputs = {column_key.value: selected_cell.value}
        from mypass_tui.ui.screens.input import InputScreen

        self.app.push_screen(
            InputScreen(title=i18n.title__edit, inputs=inputs),
            callback=callback(row_key)(self.update_cells),
        )

    def on_data_table_row_selected(self, selected_row: DataTable.RowSelected):
        row_key = selected_row.row_key

        values = self.get_row_at(selected_row.cursor_row)
        inputs = [
            InputInfo(name=col, value=val, required=req)
            for col, val, req in zip(self.column_labels, values, VaultEntry.REQUIRED)
        ]
        from mypass_tui.ui.screens.input import InputScreen

        self.app.push_screen(
            InputScreen(title=i18n.title__edit, inputs=inputs),
            callback=callback(row_key)(self.update_cells),
        )

    def action_clipboard_copy(self) -> None:
        def get_value():
            if self.cursor_type == "cell":
                value = self.get_cell_at(self.cursor_coordinate)
                return to_string(value)
            if self.cursor_type == "row":
                return ",".join(to_string(e) for e in self.get_row_at(self.cursor_row))

        pyperclip.copy(get_value())

    def action_table_mode(self):
        table = self.screen.query_one(DataTable)
        cursor = next(cursors)
        table.cursor_type = cursor

    def action_password_visibility(self):
        value = self.get_cell_at(self.cursor_coordinate)
        if isinstance(value, Password):
            value.toggle()
            self.update_cell_at(self.cursor_coordinate, value, update_width=True)
