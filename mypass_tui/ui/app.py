import threading

import darkdetect
from textual.app import App
from textual.binding import Binding
from textual.reactive import Reactive
from textual.screen import ModalScreen, Screen, ScreenResultCallbackType, ScreenResultType
from textual.widget import AwaitMount

from mypass_tui.localization import i18n
from mypass_tui.settings import bindings, settings
from mypass_tui.ui.screens import AboutScreen, HelpScreen, InputScreen, PasswordDialog, SignScreen
from mypass_tui.ui.util.session import exit_app


class MyPassApp(App):
    CSS_PATH = "mypass.css"
    TITLE = "MyPass"

    dark: Reactive[bool] = Reactive(darkdetect.isDark(), compute=False)

    App.BINDINGS = [
        Binding(bindings["quit"], "quit", i18n.footer__quit, priority=True),
        Binding(bindings["key_bindings"], "key_bindings", i18n.footer__key_binds, priority=True),
        Binding(bindings["settings"], "settings", i18n.footer__settings, priority=True),
        Binding(bindings["theme"], "toggle_dark", i18n.footer__theme, show=True),
        Binding(bindings["help"], "help_screen", i18n.footer__help),
        Binding(bindings["about"], "about_screen", i18n.footer__about),
        Binding("left", "previous_tab", show=False),
        Binding("right", "next_tab", show=False),
    ]

    def action_password_screen(self):
        def password_input(_: str | None) -> None:
            pass

        self.app.push_screen(
            PasswordDialog("Enter your master password", "Password"),
            password_input,
        )

    def push_screen(
        self,
        screen: Screen[ScreenResultType] | str,
        callback: ScreenResultCallbackType[ScreenResultType] | None = None,
    ) -> AwaitMount:
        if not isinstance(self.screen, ModalScreen):
            return super().push_screen(screen=screen, callback=callback)

    def theme_listener(self):
        def listener(theme: str) -> None:
            self.app.dark = False if theme == "Light" else True

        t = threading.Thread(target=darkdetect.listener, args=(listener,))
        t.daemon = True
        t.start()

    def on_mount(self):
        self.theme_listener()
        self.push_screen(SignScreen())

    def action_quit(self) -> None:
        exit_app(self.app)

    def action_key_bindings(self):
        def callback(inputs: dict[str, str]):
            bindings.save(inputs)

        self.push_screen(
            InputScreen(title=i18n.title__sign_in, inputs=bindings, submit_btn_text=i18n.button__save),
            callback=callback,
        )

    def action_settings(self):
        def callback(inputs: dict[str, str]):
            settings.save(inputs)

        self.push_screen(
            InputScreen(title=i18n.title__settings, inputs=settings, submit_btn_text=i18n.button__save),
            callback=callback,
        )

    def action_help_screen(self):
        self.push_screen(HelpScreen())

    def action_about_screen(self):
        self.push_screen(AboutScreen())
