from textual.app import App

from mypass_tui.globals import i18n, settings, user


def _logout_user(logout: bool):
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

        app.push_screen(QuitScreen(i18n["title"]["sign_out"], i18n["subtitle"]["confirm_sign_out"]), callback=do_it)
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
