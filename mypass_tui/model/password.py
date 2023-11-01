from enum import Enum


class Password(str):
    mask = "••••••"

    @classmethod
    def create(cls, val: str, hide: bool):
        if hide:
            return cls.create_hidden(val)
        return cls.create_visible(val)

    @classmethod
    def create_hidden(cls, val: str):
        return cls(cls.mask, val, hide=True)

    @classmethod
    def create_visible(cls, val: str):
        return cls(val, cls.mask, hide=False)

    def __new__(cls, val: str, next_val: str, hide: bool):
        instance = super().__new__(cls, val)
        instance.next_val = next_val
        instance.is_hidden = hide
        return instance

    @property
    def toggle(self):
        return Password(val=self.next_val, next_val=self, hide=not self.is_hidden)

    @property
    def visible(self):
        return self.toggle if self.is_hidden else self


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
