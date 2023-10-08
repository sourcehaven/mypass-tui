from typing import Sequence

from src.utils.string import rreplace


class ValidatorException(Exception):
    pass


class RequiredException(ValidatorException):
    
    def __init__(self, names: Sequence[str]):
        if len(names) == 0:
            raise ValueError("Must be at least one argument!")

        concat = ', '.join(names)
        concat = rreplace(concat, ",", " and", 1)

        if len(names) == 1:
            super().__init__(f"{concat} field is required!")
        else:
            super().__init__(f"{concat} fields are required!")
