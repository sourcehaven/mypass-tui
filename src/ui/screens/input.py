from textual.containers import ScrollableContainer
from textual.widgets import Button, Switch

import src.model.password as mpw
from ..widgets.epic_input import EpicInput
from ..widgets.feedback import show_feedback_on_error, Feedback
from ...exception.validator import RequiredException, ValidatorException
from ...model.input_info import InputInfo
from ...ui.screens.secondary import DialogScreen
from ...ui.widgets.input_label import InputLabel, LabeledInput, get_invalid_fields
from ...ui.widgets.password import Password
from ...utils.string import snake_case_text_to_sentence


class InputScreen(DialogScreen):

    def __init__(
            self,
            title: str,
            inputs: list[InputInfo] | dict,
            submit_btn_text: str = "Submit",
            cancel_btn_text: str = "Cancel",
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            *args, **kwargs,
    ):
        if isinstance(inputs, dict):
            inputs = [InputInfo(name=key, value=val, required=False) for key, val in inputs.items()]

        self.inputs = inputs
        self.args = args
        self.kwargs = kwargs

        super().__init__(
            title=title,
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
            elif isinstance(value, list):
                value = ", ".join(info.value)

            if isinstance(value, str):
                input_widget = EpicInput(id=info.name, value=value, classes="labeled_input")
            elif isinstance(value, mpw.Password):
                input_widget = Password(id=info.name, value=value.data, password=value.is_hidden, classes="labeled_input")
            elif isinstance(value, bool):
                input_widget = Switch(id=info.name, value=value, animate=True)
            else:
                raise ValueError(f"Invalid value: {value!r}")

            yield LabeledInput(
                InputLabel(snake_case_text_to_sentence(info.name), required=info.required),
                input_widget,
            )

    def _compose(self):
        yield ScrollableContainer(
            *self._build_content(),
            Feedback(id="inputs_feedback"),
        )

    @show_feedback_on_error(ValidatorException, selector="#inputs_feedback")
    def on_submit_pressed(self, _: Button.Pressed):
        invalid_fields = get_invalid_fields(self)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            from ..util.scrape import scrape_inputs
            inputs = scrape_inputs(self, password_to_string=False)
            self.dismiss(inputs)
