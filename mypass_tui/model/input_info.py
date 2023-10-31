import typing
from dataclasses import dataclass


@dataclass(slots=True)
class InputDetail:
    text: str
    value: typing.Any
    required: bool


def get_id_with_text(inputs: dict[str, InputDetail]):
    return {id: inp.value for id, inp in inputs.items()}
