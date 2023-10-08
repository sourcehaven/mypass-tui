from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Label, Static

from ..util.scrape import clear_inputs
from ..widgets.epic_input import EpicInput
from ..widgets.vault_table import VaultTable
from ..widgets.feedback import Feedback
from ..widgets.dynamic_text_area import DynamicTextArea
from ..widgets.feedback import show_feedback_on_error, FeedbackStyle
from ..widgets.input_label import InputLabel, LabeledInput, get_invalid_fields, get_field_value_pairs
from ..widgets.password import Password
from ... import session
from ...exception.validator import RequiredException, ValidatorException
from ...model.vault_entry import VaultEntry
from ...settings import settings

NEW_PAGE_ID = "new_page"
NEW_PAGE_TITLE = "New"


SHOW = "Show"
HIDE = "Hide"


class Gap(Static):

    DEFAULT_CSS = """
    Gap {
        height: 1; 
    }
    """


class NewEntryPage(Static):

    def compose(self) -> ComposeResult:
        yield Label("Add new vault entry", classes="title")
        with ScrollableContainer(classes="container"):
            yield LabeledInput(
                InputLabel("Username", required=True),
                EpicInput(id="username", name="username", classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel("Password", required=True),
                Password(id="password", name="password", classes="labeled_input", password_mask=settings["password_mask"]),
            )
            yield LabeledInput(
                InputLabel("Title"),
                EpicInput(id="title", name="title", classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel("Website"),
                EpicInput(id="website", name="website", classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel("Folder"),
                EpicInput(id="folder", name="folder", classes="labeled_input"),
            )
            yield Gap()
            yield LabeledInput(
                InputLabel("Notes"),
                DynamicTextArea(id="notes", name="notes", classes="labeled_text_area"),
            )
            """
            yield LabeledInput(
                InputLabel("Tags"),
                EpicInput(id="tags"),
            )
            """

        yield Button("Save", id="save_btn", variant="primary")
        yield Feedback()

    @on(Button.Pressed, "#save_btn")
    @show_feedback_on_error(ValidatorException, selector=Feedback)
    def on_save_btn_pressed(self, pressed: Button.Pressed):
        invalid_fields = get_invalid_fields(self)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = get_field_value_pairs(self)

            entry = VaultEntry.from_dict(inputs)
            session.user.vault_add(entry)

            table = self.screen.query_one(VaultTable)
            table.add_entries(entry)

            Feedback.show(self, "Vault entry created successfully!", FeedbackStyle.SUCCESS)
            clear_inputs(self)
