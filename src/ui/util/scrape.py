from typing import Iterable

from textual.dom import DOMNode
from textual.widgets import Input

from ..widgets.input_label import LabeledInput


def scrape_inputs(node: DOMNode):
    inputs: Iterable[LabeledInput] = node.query(LabeledInput)
    return {inp.input.id: inp.value for inp in inputs}


def clear_inputs(node: DOMNode):
    inputs = node.query(Input)
    for inp in inputs:
        inp.value = ""
