import os.path
from typing import Callable, Self
import re

import yaml

from mypass_tui.paths import I18N_PATH


def required_fields_feedback(text: str, *values: str):
    assert len(values) > 0, "Must be at least one argument!"

    concat = ", ".join(values)
    return fill_placeholders(text, concat)


def fill_placeholders(text: str, *values):
    for value in values:
        text = text.replace("{}", f"[bold]{value}[/bold]", 1)

    return text


def select_placeholder(text: str, *indexes: int):
    pattern = r"{([^}]+)}"
    matches = re.findall(pattern, text)

    for i, match in zip(indexes, matches):
        option = match.split("/")[i]
        text = re.sub(pattern, f"[bold][italic]{option}[/bold][/italic]", text)

    return text


def get_language_codes():
    file_names = [f for f in os.listdir(I18N_PATH) if os.path.isfile(os.path.join(I18N_PATH, f))]
    return [name.split(".")[0] for name in file_names]


class I18N(dict):

    def __init__(self, locale: str, *args, **kwargs):
        self.locale = locale
        self.listeners = []
        super().__init__(*args, **kwargs)

    def subscribe_on_locale_change(self, callback: Callable[[Self], None]):
        self.listeners.append(callback)

    def notify_listeners(self):
        for listener in self.listeners:
            listener(self)

    @staticmethod
    def load_from_file(locale: str, path: str = I18N_PATH):
        def strip_strings(data):
            if isinstance(data, str):
                return data.strip()
            elif isinstance(data, dict):
                return {key: strip_strings(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [strip_strings(item) for item in data]
            return data

        with open(os.path.join(path, f"{locale}.yml"), "r") as f:
            data = yaml.safe_load(f)

        stripped_data = strip_strings(data)
        return stripped_data

    @classmethod
    def from_file(cls, locale: str, path=I18N_PATH):
        data = cls.load_from_file(locale=locale, path=path)
        return cls(locale, data)

    def placeholder(self, *keys: str):
        from mypass_tui.globals import settings

        if settings["placeholders"]:
            placeholder = self["placeholder"]
            for key in keys:
                placeholder = placeholder[key]
            return placeholder
        return ""

    def change_locale(self, locale: str, path=I18N_PATH):
        data = self.load_from_file(locale=locale, path=path)
        self.clear()
        self.update(data)
        self.locale = locale
        self.notify_listeners()
