from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.widgets import Button, Switch, Select

import mypass_tui.model.password as mpw
from mypass_tui.ui.widgets import Password
from mypass_tui.ui.widgets.epic_input import EpicInput
from mypass_tui.ui.widgets.feedback import show_feedback_on_error, Feedback
from mypass_tui.exception.validator import RequiredException, ValidatorException
from mypass_tui.localization import i18n
from mypass_tui.model.input_info import InputInfo
from mypass_tui.settings import bindings
from mypass_tui.ui.screens.secondary import DialogScreen
from mypass_tui.ui.widgets.input_label import InputLabel, LabeledInput, get_invalid_fields
from mypass_tui.utils.string import snake_case_text_to_sentence


class InputScreen(DialogScreen):

    BINDINGS = [
        Binding(bindings["display_mode"], action="display_mode", description="Display mode", show=False)
    ]

    def get_title(self):
        return i18n.title__edit if self.editable else i18n.title__display

    def __init__(
            self,
            inputs: list[InputInfo] | dict,
            title: str = None,
            editable: bool = False,
            submit_btn_text: str = i18n.button__submit,
            cancel_btn_text: str = i18n.button__cancel,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            *args, **kwargs,
    ):
        if isinstance(inputs, dict):
            inputs = [InputInfo(name=key, value=val, required=False) for key, val in inputs.items()]

        self.inputs = inputs
        self.editable = editable
        self.args = args
        self.kwargs = kwargs

        if title is None:
            title = self.get_title()
        super().__init__(
            title=title,
            submit_btn_disabled=True if title == i18n.title__display else False,
            submit_btn_text=submit_btn_text,
            cancel_btn_text=cancel_btn_text,
            name=name,
            id=id,
            classes=classes
        )

    def _build_content(self):
        for info in self.inputs:
            value = info.value
            if info.value is None:
                value = ""

            if isinstance(value, list):
                input_widget = Select(options=[(val, val) for val in value], id=info.name, classes="labeled_input")
            elif isinstance(value, str):
                input_widget = EpicInput(id=info.name, editable=self.editable, value=value, classes="labeled_input")
            elif isinstance(value, mpw.Password):
                input_widget = Password(id=info.name, editable=self.editable, value=value.data, password=value.is_hidden, classes="labeled_input")
            elif isinstance(value, bool):
                input_widget = Switch(id=info.name, value=value, animate=True)
            else:
                raise ValueError(f"Invalid value: {value!r}")

            yield LabeledInput(
                InputLabel(snake_case_text_to_sentence(info.name), required=info.required),
                input_widget,
            )

    def action_display_mode(self):
        self.editable = not self.editable
        self.screen_title = self.get_title()
        for inp in self.query(EpicInput):
            inp.editable = self.editable
        self.query_one("#left_button").disabled = not self.editable

        if self.editable:
            Feedback.info(self, f'Switched to "Edit" mode!')
        else:
            Feedback.info(self, f'Switched to "Display" mode!')

    def _compose(self):
        yield ScrollableContainer(
            *self._build_content(),
        )
        yield Feedback(id="inputs_feedback")

    @show_feedback_on_error(ValidatorException, selector="#inputs_feedback")
    def on_submit_pressed(self, _: Button.Pressed):
        invalid_fields = get_invalid_fields(self)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            from mypass_tui.ui.util.scrape import scrape_inputs
            inputs = scrape_inputs(self, password_to_string=False)
            self.dismiss(inputs)
