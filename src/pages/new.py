from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Button, Input, Label, Static, Select, ProgressBar

from ..widgets import Feedback
from ..widgets.password import PasswordStrength, PasswordShowHide
from ..widgets.labeled_input import LabeledInput

NEW_PAGE_ID = "new_page"
NEW_PAGE_TITLE = "New"


SHOW = 'Show'
HIDE = "Hide"

GAP_SIZE = 10


class NewEntryPage(Static):

    DEFAULT_CSS = """
    #password {
        width: 80%;
    }

    #password_strength {
        margin: 0 1;
    }

    #save_btn {
        margin: 1 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Add new vault entry", classes="title")
        with ScrollableContainer(classes="container"):
            yield LabeledInput("Username", GAP_SIZE)
            yield PasswordShowHide("Password", GAP_SIZE)
            yield LabeledInput("Title", GAP_SIZE)
            yield LabeledInput("Website", GAP_SIZE)
            yield LabeledInput("Notes", GAP_SIZE)
        yield Button("Save", id="save_btn", variant="primary")
        yield Feedback()

    @on(Button.Pressed, "#save_btn")
    async def insert_entry(self, pressed: Button.Pressed):
        await self.query_one(Feedback).show("Vault entry created successfully!", 3)
