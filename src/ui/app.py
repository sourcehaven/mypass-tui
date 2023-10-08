from textual.app import App
from textual.binding import Binding
from textual.screen import ModalScreen, ScreenResultCallbackType, Screen, ScreenResultType
from textual.widget import AwaitMount

from .pages import HELP_PAGE_ID, ABOUT_PAGE_ID, HELP_PAGE_TITLE, ABOUT_PAGE_TITLE
from .screens.about import AboutScreen
from .screens.help import HelpScreen
from .screens import PasswordDialog
from .screens.settings import SettingsScreen
from .screens.sign import SignScreen
from .util.session import exit_app
from ..settings import bindings


class MyPassApp(App):
    CSS_PATH = "mypass.css"
    TITLE = "MyPass"

    App.BINDINGS = [
        Binding(bindings["quit"], "quit", "Quit", priority=True),
        Binding(bindings["settings"], "settings", "Settings", priority=True),
        Binding(bindings["help"], HELP_PAGE_ID, HELP_PAGE_TITLE),
        Binding(bindings["about"], ABOUT_PAGE_ID, ABOUT_PAGE_TITLE),
        Binding("left", "previous_tab", show=False),
        Binding("right", "next_tab", show=False),
    ]

    def action_password_screen(self):
        def password_input(password: str | None) -> None:
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

    def on_mount(self):
        self.push_screen(SignScreen())

    def action_quit(self) -> None:
        exit_app(self.app)

    def action_settings(self):
        self.push_screen(SettingsScreen())

    def action_help_page(self):
        self.push_screen(HelpScreen())

    def action_about_page(self):
        self.push_screen(AboutScreen())
