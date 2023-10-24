import os.path
import re
from functools import wraps
from typing import Callable

import yaml

from mypass_tui.paths import I18N_PATH
from mypass_tui.settings import bindings, settings


def translate(func: Callable):
    @wraps(func)
    def wrapper(self):
        def get_text() -> str:
            data = self.data
            for part in func.__name__.split("__"):
                data = data[part]
            return data

        def replace_placeholders(val: str):
            dynamic_values = func(self)
            if dynamic_values:
                if isinstance(dynamic_values, str):
                    dynamic_values = (dynamic_values,)

                for value in dynamic_values:
                    val = val.replace("{}", f"[bold]{value}[/bold]", 1)
            return val

        def create_versions(val: str):
            pattern = r"{([^}]+)}"
            matches = re.findall(pattern, val)

            if matches:
                options = matches[0].split("/")
                return [re.sub(pattern, f"[bold][italic]{option}[/bold][/italic]", val) for option in options]
            else:
                return val

        text = get_text()
        text = replace_placeholders(text)
        text = create_versions(text)

        return text

    return property(wrapper)


def get_language_codes():
    file_names = [f for f in os.listdir(I18N_PATH) if os.path.isfile(os.path.join(I18N_PATH, f))]
    return [name.split(".")[0] for name in file_names]


class I18N:
    def __init__(self, path=I18N_PATH, locale: str = settings["locale"]):
        self.data = {}
        self.path = path
        self.locale = locale
        self.set_locale(locale)

    def set_locale(self, locale: str):
        yaml_file = os.path.join(self.path, f"{locale}.yml")
        with open(yaml_file, "r") as f:
            self.data = yaml.safe_load(f)

        self.locale = locale

    @translate
    def label__username(self):
        pass

    @translate
    def label__password(self):
        pass

    @translate
    def label__first_name(self):
        pass

    @translate
    def label__last_name(self):
        pass

    @translate
    def label__email(self):
        pass

    @translate
    def label__title(self):
        pass

    @translate
    def label__website(self):
        pass

    @translate
    def label__folder(self):
        pass

    @translate
    def label__tags(self):
        pass

    @translate
    def label__notes(self):
        pass

    @translate
    def title__sign_in(self):
        pass

    @translate
    def title__sign_up(self):
        pass

    @translate
    def title__display(self):
        pass

    @translate
    def title__edit(self):
        pass

    @translate
    def title__settings(self):
        pass

    @translate
    def title__exit(self):
        pass

    @translate
    def tab__sign_in(self):
        pass

    @translate
    def tab__sign_up(self):
        pass

    @translate
    def tab__new(self):
        pass

    @translate
    def tab__table(self):
        pass

    @translate
    def tab__folder(self):
        pass

    @translate
    def tab__tile(self):
        pass

    @translate
    def tab__about(self):
        pass

    @translate
    def tab__help(self):
        pass

    @translate
    def footer__sign_in(self):
        pass

    @translate
    def footer__sign_up(self):
        pass

    @translate
    def footer__new(self):
        pass

    @translate
    def footer__table(self):
        pass

    @translate
    def footer__folder(self):
        pass

    @translate
    def footer__tile(self):
        pass

    @translate
    def footer__about(self):
        pass

    @translate
    def footer__help(self):
        pass

    @translate
    def footer__quit(self):
        pass

    @translate
    def footer__settings(self):
        pass

    @translate
    def footer__theme(self):
        pass

    @translate
    def footer__key_binds(self):
        pass

    @translate
    def button__sign_in(self):
        pass

    @translate
    def button__sign_up(self):
        pass

    @translate
    def button__quit(self):
        pass

    @translate
    def button__submit(self):
        pass

    @translate
    def button__cancel(self):
        pass

    @translate
    def button__yes(self):
        pass

    @translate
    def button__no(self):
        pass

    @translate
    def button__save(self):
        pass

    @translate
    def cut(self):
        pass

    @translate
    def copy(self):
        pass

    @translate
    def paste(self):
        pass

    @translate
    def save(self):
        pass

    @translate
    def placeholder__sign_in__username(self):
        pass

    @translate
    def placeholder__sign_in__password(self):
        pass

    @translate
    def placeholder__sign_up__username(self):
        pass

    @translate
    def placeholder__sign_up__password(self):
        pass

    @translate
    def placeholder__sign_up__first_name(self):
        pass

    @translate
    def placeholder__sign_up__last_name(self):
        pass

    @translate
    def placeholder__sign_up__email(self):
        pass

    @translate
    def placeholder__new__username(self):
        pass

    @translate
    def placeholder__new__password(self):
        pass

    @translate
    def placeholder__new__title(self):
        pass

    @translate
    def placeholder__new__website(self):
        pass

    @translate
    def placeholder__new__folder(self):
        pass

    @translate
    def placeholder__new__tags(self):
        pass

    @translate
    def placeholder__new__notes(self):
        pass

    @translate
    def subtitle__show_hide_password(self):
        return bindings["password_visibility"]

    @translate
    def subtitle__confirm_quit(self):
        pass

    @translate
    def feedback__success__new_entry(self):
        return

    @translate
    def feedback__info__display_mode(self):
        return bindings["display_mode"]


i18n = I18N(locale="hu")
