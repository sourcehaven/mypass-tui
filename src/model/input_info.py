from dataclasses import dataclass

from .password import Password


@dataclass(slots=True)
class InputInfo:
    name: str
    value: str | int | bool | list | Password | None
    required: bool
