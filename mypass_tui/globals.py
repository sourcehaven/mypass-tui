from perdict import PerDict

from mypass_tui.localization import (
    I18N,
    KEY_BINDINGS,
    KEY_SETTINGS,
    KEY_SIGN_IN,
    KEY_SIGN_UP,
    KEY_ABOUT,
    KEY_QUIT,
    KEY_SIGN_OUT,
    KEY_SELECT, KEY_THEME, KEY_TABLE_MODE, KEY_SHOW_HIDE_PASSWORD, KEY_NEXT_TAB, KEY_PREVIOUS_TAB, KEY_POP_SCREEN,
    KEY_COPY, KEY_PASTE, KEY_CUT, KEY_VAULT_NEW, KEY_VAULT_TABLE, KEY_VAULT_FOLDER, KEY_HELP, get_default_locale,
)
from mypass_tui.paths import SETTINGS_PATH, KEY_BINDINGS_PATH
from mypass_tui.model import User, InputDetail

bindings = PerDict(
    KEY_BINDINGS_PATH,
    **{
        KEY_SIGN_IN: "f1",
        KEY_SIGN_UP: "f2",
        KEY_HELP: "f8",
        KEY_ABOUT: "f9",
        KEY_SELECT: "enter",
        KEY_QUIT: "ctrl+q",
        KEY_POP_SCREEN: "escape",
        KEY_SIGN_OUT: "ctrl+l",
        KEY_COPY: "ctrl+c",
        KEY_PASTE: "ctrl+v",
        KEY_CUT: "ctrl+x",
        KEY_VAULT_NEW: "f1",
        KEY_VAULT_TABLE: "f2",
        KEY_VAULT_FOLDER: "f3",
        KEY_PREVIOUS_TAB: "left",
        KEY_NEXT_TAB: "right",
        KEY_SHOW_HIDE_PASSWORD: "ctrl+p",
        KEY_BINDINGS: "ctrl+b",
        KEY_TABLE_MODE: "z",
        KEY_SETTINGS: "ctrl+s",
        KEY_THEME: "ctrl+t",
    }
)

settings = PerDict(SETTINGS_PATH, password_mask="•", confirm_quit=True, placeholders=False, locale=get_default_locale())

i18n = I18N.from_file(settings["locale"])

_user: User | None = None

_host = None
_port = None


def set_host(__host, /):
    global _host
    _host = __host


def set_port(__port, /):
    global _port
    _port = __port


def get_port():
    return _port


def get_host():
    return _host


def set_user(__user: User, /):
    global _user
    _user = __user


def get_user():
    return _user


def get_bindings_info():
    bindings_info = {
        id: InputDetail(text=i18n[KEY_BINDINGS][id], value=value, required=False) for id, value in bindings.items()
    }
    return bindings_info


def get_settings_info():
    settings_info = {
        id: InputDetail(text=i18n[KEY_SETTINGS][id], value=value, required=False) for id, value in settings.items()
    }
    return settings_info
