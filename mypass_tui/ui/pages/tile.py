from textual.app import ComposeResult
from textual.widgets import Label, Static

TILE_PAGE_ID = "tile_page"


class TilePage(Static):
    def compose(self) -> ComposeResult:
        yield Label("Tile page")
