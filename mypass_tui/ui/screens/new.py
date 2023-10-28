from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Label, Static

from mypass_tui.exception import RequiredException, ValidatorException
from mypass_tui.globals import i18n, user
from mypass_tui.model import VaultEntry
from mypass_tui.model.vault_entry import USERNAME, PASSWORD, TITLE, WEBSITE, FOLDER, TAGS, NOTES
from mypass_tui.ui.util.scrape import clear_inputs, scrape_inputs
from mypass_tui.ui.widgets import (
    Gap,
    InputLabel,
    LabeledInput,
    MultilineInput,
    EpicInput,
    Feedback,
    Password,
    VaultTable,
)

NEW_PAGE_ID = "new_page"


class NewEntryPage(Static):
    def compose(self) -> ComposeResult:
        yield Label(i18n["title"]["new"], classes="title")
        with ScrollableContainer(classes="container"):
            yield LabeledInput(
                InputLabel(i18n["label"]["username"], required=True),
                EpicInput(id=USERNAME, placeholder=i18n.placeholder("new", "username"), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n["label"]["password"], required=True),
                Password(id=PASSWORD, placeholder=i18n.placeholder("new", "password"), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n["label"]["title"]),
                EpicInput(id=TITLE, placeholder=i18n.placeholder("new", "title"), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n["label"]["website"]),
                EpicInput(id=WEBSITE, placeholder=i18n.placeholder("new", "website"), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n["label"]["folder"]),
                EpicInput(id=FOLDER, placeholder=i18n.placeholder("new", "folder"), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n["label"]["tags"]),
                EpicInput(id=TAGS, placeholder=i18n.placeholder("new", "tags"), classes="labeled_input"),
            )
            yield Gap()
            yield LabeledInput(
                InputLabel(i18n["label"]["notes"]),
                MultilineInput(id=NOTES, classes="labeled_text_area"),
            )

        yield Button(i18n["button"]["save"], id="save_btn", variant="primary")
        yield Feedback(id="new_feedback")

    @on(Button.Pressed, "#save_btn")
    @Feedback.on_error(ValidatorException, selector="#new_feedback")
    def on_save_btn_pressed(self, _: Button.Pressed):
        invalid_fields = LabeledInput.get_invalid_fields(self)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = scrape_inputs(self)

            entry = VaultEntry.from_dict(inputs)
            user.vault_add(entry)

            table = self.screen.query_one(VaultTable)
            table.add_entries(entry)

            Feedback.success(self, i18n["feedback"]["success"]["new_entry"])
            clear_inputs(self)
