from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Input, Label, TabPane

from ..widgets import Feedback

NEW_TAB_ID = "new_tab"
NEW_TAB_TITLE = "New"


class NewTabPane(TabPane):
    def compose(self) -> ComposeResult:
        yield Label("Add new vault entry", classes="title")
        with ScrollableContainer(classes="container"):
            yield Input(placeholder="Enter title...")
            yield Input(placeholder="Enter username...")
            yield Input(placeholder="Enter website...")
        yield Button("Save", id="save", variant="primary")
        yield Feedback()

    @on(Button.Pressed, "#save")
    async def insert_entry(self):
        await self.query_one(Feedback).show("Vault entry created successfully!", 3)
