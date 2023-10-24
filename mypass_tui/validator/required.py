from textual.validation import ValidationResult, Validator


class RequiredValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        return self.success() if value else self.failure("Field is required!")
