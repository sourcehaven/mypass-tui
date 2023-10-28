import threading

import darkdetect
from textual.app import App
from textual.binding import Binding
from textual.reactive import Reactive
from textual.screen import ModalScreen, Screen, ScreenResultCallbackType, ScreenResultType
from textual.widget import AwaitMount

from mypass_tui.globals import i18n, bindings, settings, get_bindings_info, get_settings_info
from mypass_tui.localization import get_language_codes
from mypass_tui.model import DefaultList
from mypass_tui.ui.screens import AboutScreen, HelpScreen, InputScreen, SignScreen
from mypass_tui.ui.util.session import exit_app


class MyPassApp(App):
    CSS_PATH = "mypass.css"
    TITLE = "MyPass"

    dark: Reactive[bool] = Reactive(darkdetect.isDark(), compute=False)

    App.BINDINGS = [
        Binding(bindings["quit"], "quit", i18n["footer"]["quit"], priority=True, show=True),
        Binding(bindings["key_bindings"], "key_bindings", i18n["footer"]["key_binds"], priority=True, show=True),
        Binding(bindings["settings"], "settings", i18n["footer"]["settings"], priority=True, show=True),
        Binding(bindings["theme"], "toggle_dark", i18n["footer"]["theme"], priority=True, show=True),
        Binding(bindings["help"], "help_screen", i18n["footer"]["help"], priority=True, show=True),
        Binding(bindings["about"], "about_screen", i18n["footer"]["about"], priority=True, show=True),
        Binding("left", "previous_tab", show=False),
        Binding("right", "next_tab", show=False),
    ]

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
        def refresh_app(*args, **kwargs):
            self.app.refresh(repaint=True, layout=True)

        self.theme_listener()
        i18n.subscribe_on_locale_change(refresh_app)
        self.push_screen(SignScreen())

    def action_quit(self) -> None:
        exit_app(self.app)

    def action_key_bindings(self):
        def callback(inputs: dict[str, str]):
            bindings.save(inputs)

        self.push_screen(
            InputScreen(title=i18n["title"]["key_bindings"], inputs=get_bindings_info(), submit_btn_text=i18n["button"]["save"]),
            callback=callback,
        )

    def action_settings(self):
        def callback(inputs: dict[str, str]):
            settings.save(inputs)

        settings_info = get_settings_info()

        settings_info["locale"].value = DefaultList(get_language_codes(), settings_info["locale"].value)

        self.push_screen(
            InputScreen(title=i18n["title"]["settings"], inputs=settings_info, submit_btn_text=i18n["button"]["save"]),
            callback=callback,
        )

    def action_help_screen(self):
        self.push_screen(HelpScreen())

    def action_about_screen(self):
        self.push_screen(AboutScreen())
