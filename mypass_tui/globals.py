from perdict import PerDict

from mypass_tui.localization import I18N
from mypass_tui.paths import SETTINGS_PATH, KEY_BINDINGS_PATH
from mypass_tui.model import User, InputInfo

bindings = PerDict(
    KEY_BINDINGS_PATH,
    sign_in="f1",
    sign_up="f2",
    help="f8",
    about="f9",
    select="enter",
    quit="ctrl+q",
    pop_screen="escape",
    sign_out="ctrl+l",
    copy="ctrl+c",
    paste="ctrl+v",
    cut="ctrl+x",
    vault_new="f1",
    vault_table="f2",
    vault_folder="f3",
    previous_tab="left",
    next_tab="right",
    password_visibility="ctrl+p",
    key_bindings="ctrl+b",
    table_mode="z",
    settings="ctrl+s",
    theme="ctrl+t",
)

settings = PerDict(
    SETTINGS_PATH,
    password_mask="•",
    confirm_quit=True,
    placeholders=False,
    locale="en"
)

i18n = I18N.from_file(settings["locale"])

user: User | None = None


def set_user(_user: User, /):
    global user
    user = _user


def get_bindings_info():
    bindings_info = {
        id: InputInfo(text=i18n["binding"][id], value=value, required=False)
        for id, value in bindings.items()
    }
    return bindings_info


def get_settings_info():
    settings_info = {
        id: InputInfo(text=i18n["setting"][id], value=value, required=False)
        for id, value in settings.items()
    }
    return settings_info
