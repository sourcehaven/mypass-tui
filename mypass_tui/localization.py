import os.path
from typing import Callable, Self, Any, Final
import re
import locale

import yaml

from mypass_tui.paths import I18N_PATH

KEY_SIGNIN: Final = "sign_in"
KEY_SIGNOUT: Final = "sign_out"
KEY_SIGNUP: Final = "sign_up"
KEY_LABEL: Final = "label"
KEY_FOOTER: Final = "footer"
KEY_BUTTON: Final = "button"
KEY_TITLE: Final = "title"
KEY_TAB: Final = "tab"
KEY_PLACEHOLDER: Final = "placeholder"
KEY_FEEDBACK: Final = "feedback"
KEY_SUBTITLE: Final = "subtitle"
KEY_BINDINGS: Final = "key_bindings"
KEY_SETTINGS: Final = "settings"
KEY_ABOUT: Final = "about"
KEY_QUIT: Final = "quit"
KEY_SELECT: Final = "select"
KEY_THEME: Final = "toggle_dark"
KEY_SAVE: Final = "save"
KEY_LOCALE: Final = "locale"
KEY_HELP: Final = "help"
KEY_TABLE_MODE: Final = "table_mode"
KEY_SHOW_HIDE_PASSWORD: Final = "password_visibility"
KEY_NEXT_TAB: Final = "next_tab"
KEY_PREVIOUS_TAB: Final = "previous_tab"
KEY_COPY: Final = "copy"
KEY_PASTE: Final = "paste"
KEY_CUT: Final = "cut"
KEY_POP_SCREEN: Final = "pop_screen"
KEY_VAULT_NEW: Final = "vault_new"
KEY_VAULT_TABLE: Final = "vault_table"
KEY_VAULT_FOLDER: Final = "vault_folder"


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


def get_available_language_codes():
    file_names = [f for f in os.listdir(I18N_PATH) if os.path.isfile(os.path.join(I18N_PATH, f))]
    return [name.split(".")[0] for name in file_names]


def get_default_locale():
    system_locale = locale.getlocale()[0].split("_")[0]
    supported_locales = get_available_language_codes()
    if system_locale in supported_locales:
        return system_locale
    return "en"


class I18N(dict[str, Any]):

    def __init__(self, locale: str, *args, **kwargs):
        self.locale = locale
        self.listeners = []
        super().__init__(*args, **kwargs)

    def vault_entry_labels(self):
        from mypass_tui.model.vault_entry import USERNAME, PASSWORD, TITLE, WEBSITE, FOLDER, NOTES, TAGS

        label = self[KEY_LABEL]
        texts = (
            label[USERNAME],
            label[PASSWORD],
            label[TITLE],
            label[WEBSITE],
            label[FOLDER],
            label[NOTES],
            label[TAGS],
        )
        return texts

    def user_labels(self):
        from mypass_tui.model.user import USERNAME, PASSWORD, FIRSTNAME, LASTNAME, EMAIL

        label = self[KEY_LABEL]
        texts = (
            label[USERNAME],
            label[PASSWORD],
            label[FIRSTNAME],
            label[LASTNAME],
            label[EMAIL],
        )
        return texts

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
        if locale != self.locale:
            data = self.load_from_file(locale=locale, path=path)
            self.clear()
            self.update(data)
            self.locale = locale
            self.notify_listeners()
            return True
        return False
