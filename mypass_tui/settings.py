from perdict import PerDict

from mypass_tui.paths import KEY_BINDINGS_PATH, SETTINGS_PATH

bindings = PerDict(
    KEY_BINDINGS_PATH,
    sign_in="1",
    sign_up="2",
    select="enter",
    quit="ctrl+q",
    pop_screen="escape",
    sign_out="ctrl+l",
    help="f1",
    about="f2",
    copy="ctrl+c",
    paste="ctrl+v",
    cut="ctrl+x",
    vault_new="1",
    vault_table="2",
    vault_tree="3",
    previous_tab="left",
    next_tab="right",
    password_visibility="ctrl+p",
    key_bindings="ctrl+b",
    table_mode="z",
    settings="ctrl+s",
    theme="ctrl+t",
    display_mode="ctrl+e",
)

settings = PerDict(
    SETTINGS_PATH,
    password_mask="•",
    confirm_quit=True,
    placeholders=True,
)
