from typing import Iterable

from textual.dom import DOMNode
from textual.widgets import Input

from mypass_tui.model import InputDetail, Password
from mypass_tui.ui.widgets.input_label import LabeledInput
from mypass_tui.utils.string import to_string


def scrape_inputs(node: DOMNode, password_value=False) -> dict[str, InputDetail]:
    inputs: Iterable[LabeledInput] = node.query(LabeledInput)
    ret: dict[str, InputDetail] = {
        inp.input.id: InputDetail(text=inp.label.text, value=inp.value, required=inp.label.required)
        for inp in inputs
    }

    if password_value:
        for k, details in ret.items():
            value = details.value
            if isinstance(value, Password):
                if value.is_hidden:
                    details.value = value.toggle

    return ret


def clear_inputs(node: DOMNode):
    inputs = node.query(Input)
    for inp in inputs:
        inp.value = ""
