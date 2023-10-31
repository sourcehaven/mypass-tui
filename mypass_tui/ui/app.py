import threading

import darkdetect
from textual.app import App
from textual.binding import Binding
from textual.reactive import Reactive
from textual.screen import ModalScreen, Screen, ScreenResultCallbackType, ScreenResultType
from textual.widget import AwaitMount

from mypass_tui.globals import i18n, bindings, settings, get_bindings_info, get_settings_info
from mypass_tui.localization import (
    get_available_language_codes,
    KEY_BUTTON, KEY_TITLE, KEY_FOOTER, KEY_ABOUT, KEY_BINDINGS,
    KEY_SETTINGS, KEY_QUIT, KEY_HELP, KEY_THEME, KEY_SAVE,
    KEY_LOCALE
)
from mypass_tui.model import DefaultList, InputDetail
from mypass_tui.model.input_info import get_id_with_text
from mypass_tui.ui.screens import AboutScreen, HelpScreen, InputScreen, SignScreen, RestartScreen
from mypass_tui.ui.util.session import exit_app


class MyPassApp(App):
    CSS_PATH = "mypass.css"
    TITLE = "MyPass"

    dark: Reactive[bool] = Reactive(darkdetect.isDark(), compute=False)

    App.BINDINGS = [
        Binding(bindings[KEY_QUIT], KEY_QUIT, i18n[KEY_FOOTER][KEY_QUIT], priority=True, show=True),
        Binding(bindings[KEY_BINDINGS], KEY_BINDINGS, i18n[KEY_FOOTER][KEY_BINDINGS], priority=True, show=True),
        Binding(bindings[KEY_SETTINGS], KEY_SETTINGS, i18n[KEY_FOOTER][KEY_SETTINGS], priority=True, show=True),
        Binding(bindings[KEY_THEME], KEY_THEME, i18n[KEY_FOOTER][KEY_THEME], priority=True, show=True),
        Binding(bindings[KEY_HELP], KEY_HELP, i18n[KEY_FOOTER][KEY_HELP], priority=True, show=True),
        Binding(bindings[KEY_ABOUT], KEY_ABOUT, i18n[KEY_FOOTER][KEY_ABOUT], priority=True, show=True),
    ]

    def push_screen(
        self,
        screen: Screen[ScreenResultType] | str,
        callback: ScreenResultCallbackType[ScreenResultType] | None = None,
        wait_for_dismiss: bool = False,
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
        async def callback(new_bindings_details: dict[str, InputDetail]):
            new_bindings = get_id_with_text(new_bindings_details)
            if new_bindings != bindings:
                bindings.save(new_bindings)
                await self.push_screen(RestartScreen())

        self.push_screen(
            InputScreen(title=i18n[KEY_TITLE][KEY_BINDINGS], inputs=get_bindings_info(), submit_btn_text=i18n[KEY_BUTTON][KEY_SAVE]),
            callback=callback,
        )

    def action_settings(self):
        async def callback(new_setting_details: dict[str, InputDetail]):
            new_settings = get_id_with_text(new_setting_details)
            if new_settings != settings:
                settings.save(new_settings)
                await self.push_screen(RestartScreen())

        settings_info = get_settings_info()
        settings_info[KEY_LOCALE].value = DefaultList(get_available_language_codes(), settings_info[KEY_LOCALE].value)

        self.push_screen(
            InputScreen(title=i18n[KEY_TITLE][KEY_SETTINGS], inputs=settings_info, submit_btn_text=i18n[KEY_BUTTON][KEY_SAVE]),
            callback=callback,
        )

    def action_help(self):
        self.push_screen(HelpScreen())

    def action_about(self):
        self.push_screen(AboutScreen())
