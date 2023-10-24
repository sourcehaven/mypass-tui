from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Label, Static

from mypass_tui import session
from mypass_tui.exception.validator import RequiredException, ValidatorException
from mypass_tui.localization import i18n
from mypass_tui.model.vault_entry import VaultEntry

from mypass_tui.ui.util.scrape import clear_inputs, scrape_inputs
from mypass_tui.ui.widgets.epic_input import EpicInput
from mypass_tui.ui.widgets.gap import Gap
from mypass_tui.ui.widgets.vault_table import VaultTable
from mypass_tui.ui.widgets.feedback import Feedback
from mypass_tui.ui.widgets.dynamic_text_area import DynamicTextArea
from mypass_tui.ui.widgets.feedback import show_feedback_on_error
from mypass_tui.ui.widgets.input_label import InputLabel, LabeledInput, get_invalid_fields
from mypass_tui.ui.widgets.password import Password


NEW_PAGE_ID = "new_page"


SHOW = "Show"
HIDE = "Hide"


class NewEntryPage(Static):

    def compose(self) -> ComposeResult:
        yield Label("Add new vault entry", classes="title")
        with ScrollableContainer(classes="container"):
            yield LabeledInput(
                InputLabel(i18n.label__username, required=True),
                EpicInput(id="username", placeholder=i18n.placeholder__new__username, classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n.label__password, required=True),
                Password(id="password", placeholder=i18n.placeholder__new__password, classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n.label__title),
                EpicInput(id="title", placeholder=i18n.placeholder__new__title, classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n.label__website),
                EpicInput(id="website", placeholder=i18n.placeholder__new__website, classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n.label__folder),
                EpicInput(id="folder", placeholder=i18n.placeholder__new__folder, classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n.label__tags),
                EpicInput(id="tags", placeholder=i18n.placeholder__new__tags, classes="labeled_input"),
            )
            yield Gap()
            yield LabeledInput(
                InputLabel(i18n.label__notes),
                DynamicTextArea(id="notes", classes="labeled_text_area"),
            )

        yield Button(i18n.button__save, id="save_btn", variant="primary")
        yield Feedback()

    @on(Button.Pressed, "#save_btn")
    @show_feedback_on_error(ValidatorException, selector=Feedback)
    def on_save_btn_pressed(self, _: Button.Pressed):
        invalid_fields = get_invalid_fields(self)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = scrape_inputs(self)

            entry = VaultEntry.from_dict(inputs)
            session.user.vault_add(entry)

            table = self.screen.query_one(VaultTable)
            table.add_entries(entry)

            Feedback.success(self, i18n.feedback__success__new_entry)
            clear_inputs(self)
