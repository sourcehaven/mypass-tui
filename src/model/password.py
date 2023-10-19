from collections import UserString
from enum import Enum


class Password(UserString):
    mask = "••••••••"

    def __init__(self, _value: str, /, hide=True):
        if _value is None:
            _value = ""

        super().__init__(_value)
        self.is_hidden = hide

    def __str__(self):
        return Password.mask if self.is_hidden else self.data

    def toggle(self):
        self.is_hidden = not self.is_hidden


class PasswordStrength(Enum):
    NOT_SET = 0
    WEAK = 1
    MEDIUM = 2
    STRONG = 3
    VERY_STRONG = 4

    def __str__(self):
        if self.value == 0:
            return ""
        return self.name.capitalize().replace("_", " ")


def default_get_password_strength(password: str):
    if len(password) == 0:
        return PasswordStrength.NOT_SET

    if len(password) < 8:
        return PasswordStrength.WEAK
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(not char.isalnum() for char in password)

    if has_lowercase and has_uppercase and has_digit and has_special:
        return PasswordStrength.VERY_STRONG
    elif has_lowercase and has_uppercase and has_digit:
        return PasswordStrength.STRONG
    elif (has_lowercase or has_uppercase) and has_digit:
        return PasswordStrength.MEDIUM
    else:
        return PasswordStrength.WEAK
