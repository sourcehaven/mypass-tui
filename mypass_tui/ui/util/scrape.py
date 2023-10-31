from typing import Iterable

from textual.dom import DOMNode
from textual.widgets import Input

from mypass_tui.model import InputDetail
from mypass_tui.ui.widgets.input_label import LabeledInput
from mypass_tui.utils.string import to_string


def scrape_inputs(node: DOMNode, password_to_string=True) -> dict[str, InputDetail]:
    def user_string_to_string(val):
        if password_to_string:
            return to_string(val)
        return val

    inputs: Iterable[LabeledInput] = node.query(LabeledInput)
    return {
        inp.input.id: InputDetail(text=inp.label.text, value=user_string_to_string(inp.value), required=inp.label.required)
        for inp in inputs
    }


def clear_inputs(node: DOMNode):
    inputs = node.query(Input)
    for inp in inputs:
        inp.value = ""
