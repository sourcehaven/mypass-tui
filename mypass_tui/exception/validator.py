from typing import Sequence


class ValidatorException(Exception):
    pass


class RequiredException(ValidatorException):
    def __init__(self, values: Sequence[str]):
        from mypass_tui.globals import i18n
        from mypass_tui.localization import fill_placeholders

        assert len(values) > 0, "Must be at least one argument!"

        if len(values) == 1:
            key = "field_is_required"
        else:
            key = "fields_are_required"

        super().__init__(fill_placeholders(i18n[key], ", ".join(values)))
