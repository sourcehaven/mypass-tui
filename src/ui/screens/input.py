from textual.containers import ScrollableContainer
from textual.widgets import Button

from ..widgets.epic_input import EpicInput
from ..widgets.feedback import show_feedback_on_error, Feedback
from ...exception.validator import RequiredException, ValidatorException
from ...model.password import Password as ModelPassword
from ...ui.screens.secondary import DialogScreen
from ...ui.widgets.input_label import InputLabel, LabeledInput, get_invalid_fields, get_field_value_pairs
from ...ui.widgets.password import Password


class InputScreen(DialogScreen):

    def __init__(self, title: str, inputs: list[tuple[str, str, bool]]):
        super().__init__(title)
        self.inputs = inputs

    @show_feedback_on_error(ValidatorException, selector="#inputs_feedback")
    def on_submit_pressed(self, _: Button.Pressed):
        invalid_fields = get_invalid_fields(self)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = get_field_value_pairs(self)
            self.dismiss(inputs)

    def _compose(self):
        def generate_labeled_inputs():
            for label, value, required in self.inputs:
                if value is None:
                    value = ""
                elif isinstance(value, str):
                    value = value
                elif isinstance(value, ModelPassword):
                    value = value.data
                elif isinstance(value, list):
                    value = ', '.join(value)

                kwargs = {"id": label, "name": label, "value": value}
                if isinstance(value, ModelPassword):
                    input_widget = Password(**kwargs)
                else:
                    input_widget = EpicInput(**kwargs)

                yield LabeledInput(
                    InputLabel(label, required=required),
                    input_widget,
                )
        yield ScrollableContainer(
            *generate_labeled_inputs(),
            Feedback(id="inputs_feedback"),
        )
