from textual.validation import Validator, ValidationResult


class RequiredValidator(Validator):

    def validate(self, value: str) -> ValidationResult:
        return self.success() if value else self.failure("Field is required!")
