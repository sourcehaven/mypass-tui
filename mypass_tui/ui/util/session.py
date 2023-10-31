import os
import sys

from textual.app import App

from mypass_tui.globals import i18n, settings, get_user
from mypass_tui.localization import KEY_TITLE, KEY_SUBTITLE


def _logout_user(logout: bool):
    user = get_user()
    if user is not None and logout:
        user.logout()


def sign_out(app: App, logout=True):
    def do_it(_quit=True):
        if _quit:
            from mypass_tui.ui.screens import SignScreen

            _logout_user(logout)
            app.switch_screen(SignScreen())

    if settings.get("confirm_quit"):
        from mypass_tui.ui.screens import QuitScreen

        app.push_screen(QuitScreen(i18n[KEY_TITLE]["sign_out"], i18n[KEY_SUBTITLE]["confirm_sign_out"]), callback=do_it)
    else:
        do_it()


def exit_app(app: App, logout=True):
    def do_it(_quit=True):
        if _quit:
            _logout_user(logout)
            app.exit()

    if settings.get("confirm_quit"):
        from mypass_tui.ui.screens import QuitScreen

        app.push_screen(QuitScreen(), callback=do_it)
    else:
        do_it()


def restart_app(app: App):
    app.exit()
    os.execv(sys.executable, ['python'] + sys.argv)
