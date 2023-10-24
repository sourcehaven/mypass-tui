from textual.app import ComposeResult
from textual.widgets import Static, Input

TILE_PAGE_ID = "tile_page"


class TilePage(Static):

    def compose(self) -> ComposeResult:
        self.input_prompt = Input(id="tile_prompt")
        yield self.input_prompt
