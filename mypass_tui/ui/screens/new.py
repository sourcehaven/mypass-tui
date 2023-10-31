from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Label, Static

from mypass_tui.exception import RequiredException, ValidatorException
from mypass_tui.globals import i18n, get_user
from mypass_tui.localization import KEY_LABEL, KEY_FEEDBACK, KEY_BUTTON
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
        yield Label(i18n[TITLE]["new"], classes="title")
        with ScrollableContainer(classes="container"):
            yield LabeledInput(
                InputLabel(i18n[KEY_LABEL][USERNAME], required=True),
                EpicInput(id=USERNAME, placeholder=i18n.placeholder("new", USERNAME), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n[KEY_LABEL][PASSWORD], required=True),
                Password(id=PASSWORD, placeholder=i18n.placeholder("new", PASSWORD), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n[KEY_LABEL][TITLE]),
                EpicInput(id=TITLE, placeholder=i18n.placeholder("new", TITLE), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n[KEY_LABEL][WEBSITE]),
                EpicInput(id=WEBSITE, placeholder=i18n.placeholder("new", WEBSITE), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n[KEY_LABEL][FOLDER]),
                EpicInput(id=FOLDER, placeholder=i18n.placeholder("new", FOLDER), classes="labeled_input"),
            )
            yield LabeledInput(
                InputLabel(i18n[KEY_LABEL][TAGS]),
                EpicInput(id=TAGS, placeholder=i18n.placeholder("new", TAGS), classes="labeled_input"),
            )
            yield Gap()
            yield LabeledInput(
                InputLabel(i18n[KEY_LABEL][NOTES]),
                MultilineInput(id=NOTES, classes="labeled_text_area"),
            )

        yield Button(i18n[KEY_BUTTON]["save"], id="save_btn", variant="primary")
        yield Feedback(id="new_feedback")

    @on(Button.Pressed, "#save_btn")
    @Feedback.on_error(ValidatorException, selector="#new_feedback")
    def on_save_btn_pressed(self, _: Button.Pressed):
        invalid_fields = LabeledInput.get_invalid_fields(self)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = scrape_inputs(self)
            inputs = {id: inp.text for id, inp in inputs.items()}
            entry = VaultEntry.from_dict(inputs)
            get_user().vault_add(entry)

            table = self.screen.query_one(VaultTable)
            table.add_entries(entry)

            Feedback.success(self, i18n[KEY_FEEDBACK]["success"]["new_entry"])
            clear_inputs(self)
