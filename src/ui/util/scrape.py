from typing import Iterable

from textual.dom import DOMNode
from textual.widgets import Input

from ..widgets.input_label import LabeledInput
from ...model.password import Password
from ...utils.string import to_string


def scrape_inputs(node: DOMNode, password_to_string=True):
    def user_string_to_string(val):
        if password_to_string:
            return to_string(val)
        return val

    inputs: Iterable[LabeledInput] = node.query(LabeledInput)
    return {inp.input.id: user_string_to_string(inp.value) for inp in inputs}


def clear_inputs(node: DOMNode):
    inputs = node.query(Input)
    for inp in inputs:
        inp.value = ""
