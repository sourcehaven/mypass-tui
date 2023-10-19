from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Label, Static

from ..util.scrape import clear_inputs, scrape_inputs
from ..widgets.epic_input import EpicInput
from ..widgets.gap import Gap
from ..widgets.vault_table import VaultTable
from ..widgets.feedback import Feedback
from ..widgets.dynamic_text_area import DynamicTextArea
from ..widgets.feedback import show_feedback_on_error, FeedbackStyle
from ..widgets.input_label import InputLabel, LabeledInput, get_invalid_fields
from ..widgets.password import Password
from ... import session
from ...exception.validator import RequiredException, ValidatorException
from ...model.vault_entry import VaultEntry

NEW_PAGE_ID = "new_page"
NEW_PAGE_TITLE = "New"


SHOW = "Show"
HIDE = "Hide"


class NewEntryPage(Static):

    def compose(self) -> ComposeResult:
        yield Label("Add new vault entry", classes="title")
        with ScrollableContainer(classes="container"):
            yield LabeledInput(
                InputLabel("Username", required=True),
                EpicInput(id="username", placeholder="new_username", classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel("Password", required=True),
                Password(id="password", placeholder="new_password", classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel("Title"),
                EpicInput(id="title", placeholder="new_title", classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel("Website"),
                EpicInput(id="website", placeholder="new_website", classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel("Folder"),
                EpicInput(id="folder", placeholder="new_folder", classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel("Tags"),
                EpicInput(id="tags", placeholder="new_tags", classes="labeled_input"),
            )
            yield Gap()
            yield LabeledInput(
                InputLabel("Notes"),
                DynamicTextArea(id="notes", classes="labeled_text_area"),
            )

        yield Button("Save", id="save_btn", variant="primary")
        yield Feedback()

    @on(Button.Pressed, "#save_btn")
    @show_feedback_on_error(ValidatorException, selector=Feedback)
    def on_save_btn_pressed(self, pressed: Button.Pressed):
        invalid_fields = get_invalid_fields(self)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = scrape_inputs(self)

            entry = VaultEntry.from_dict(inputs)
            session.user.vault_add(entry)

            table = self.screen.query_one(VaultTable)
            table.add_entries(entry)

            Feedback.show(self, "Vault entry created successfully!", FeedbackStyle.SUCCESS)
            clear_inputs(self)
