from textual.containers import ScrollableContainer
from textual.widgets import Button, Select, Switch

import mypass_tui.model.password as mpw
from mypass_tui.exception.validator import RequiredException, ValidatorException
from mypass_tui.globals import i18n
from mypass_tui.model import InputInfo, DefaultList
from mypass_tui.ui.screens import DialogScreen
from mypass_tui.ui.widgets import EpicInput, Feedback, Password, InputLabel, LabeledInput


class InputScreen(DialogScreen):
    def __init__(
        self,
        title: str,
        inputs: dict[str, InputInfo],
        submit_btn_text: str = i18n["button"]["submit"],
        cancel_btn_text: str = i18n["button"]["cancel"],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        *args,
        **kwargs,
    ):
        self.inputs = inputs
        self.args = args
        self.kwargs = kwargs

        super().__init__(
            title=title,
            submit_btn_text=submit_btn_text,
            cancel_btn_text=cancel_btn_text,
            name=name,
            id=id,
            classes=classes,
        )

    def _build_content(self):
        for id, info in self.inputs.items():
            if info.value is None:
                value = ''
            else:
                value = info.value

            if isinstance(value, DefaultList):
                input_widget = Select(id=id, options=[(val, val) for val in value], value=value.default_value, allow_blank=False, classes="labeled_input")
            elif isinstance(value, str):
                input_widget = EpicInput(id=id, value=value, classes="labeled_input")
            elif isinstance(value, mpw.Password):
                input_widget = Password(id=id, value=value.data, password=value.is_hidden, classes="labeled_input")
            elif isinstance(value, bool):
                input_widget = Switch(id=id, value=value, animate=True)
            else:
                raise ValueError(f"Invalid value: {value!r}")

            yield LabeledInput(
                InputLabel(info.text, required=info.required),
                input_widget,
            )

    def _compose(self):
        yield ScrollableContainer(
            *self._build_content(),
        )
        yield Feedback(id="inputs_feedback")

    @Feedback.on_error(ValidatorException, selector="#inputs_feedback")
    def on_submit_pressed(self, _: Button.Pressed):
        invalid_fields = LabeledInput.get_invalid_fields(self)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            from mypass_tui.ui.util.scrape import scrape_inputs

            inputs = scrape_inputs(self, password_to_string=False)
            self.dismiss(inputs)
