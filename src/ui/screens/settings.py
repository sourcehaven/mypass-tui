from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button

from .secondary import DialogScreen
from ..util.format import snake_case_text_to_sentence
from ..util.scrape import scrape_inputs
from ..widgets.epic_input import EpicInput
from ..widgets.input_label import InputLabel, LabeledInput
from ...settings import bindings


class SettingsScreen(DialogScreen):

    def __init__(self):
        super().__init__(
            title="Shortcut keys",
            submit_btn_text="Save",
            cancel_btn_text="Cancel",
        )

    def _compose(self) -> ComposeResult:
        inputs = (
            LabeledInput(
                InputLabel(snake_case_text_to_sentence(key)),
                EpicInput(value=value, id=key, classes="labeled_input"),
            )
            for key, value in bindings.items()
        )

        yield ScrollableContainer(*inputs)

    def on_submit_pressed(self, _: Button.Pressed):
        inputs = scrape_inputs(self)
        bindings.save(inputs)
        self.dismiss(inputs)
