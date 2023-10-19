from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen, ScreenResultCallbackType, Screen, ScreenResultType
from textual.widget import AwaitMount

from .pages import HELP_PAGE_ID, ABOUT_PAGE_ID, HELP_PAGE_TITLE, ABOUT_PAGE_TITLE
from .screens.about import AboutScreen
from .screens.help import HelpScreen
from .screens import PasswordDialog
from .screens.input import InputScreen
from .screens.sign import SignScreen
from .util.session import exit_app
from .widgets import VaultTable
from ..model.password import Password
from ..model.vault_entry import VaultEntry
from ..settings import bindings, settings


class MyPassApp(App):
    CSS_PATH = "mypass.css"
    TITLE = "MyPass"

    App.BINDINGS = [
        Binding(bindings["quit"], "quit", "Quit", priority=True),
        Binding(bindings["key_bindings"], "key_bindings", "Key bindings", priority=True),
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

    def compose(self) -> ComposeResult:
        yield VaultTable([VaultEntry(id=5, username="User1", password=Password("Passwd"))])

    def action_quit(self) -> None:
        exit_app(self.app)

    def action_key_bindings(self):
        def callback(inputs: dict[str, str]):
            bindings.save(inputs)

        self.push_screen(InputScreen("Key bindings", bindings, submit_btn_text="Save"), callback=callback)

    def action_settings(self):
        def callback(inputs: dict[str, str]):
            settings.save(inputs)

        self.push_screen(InputScreen("Settings", settings, submit_btn_text="Save"), callback=callback)

    def action_help_page(self):
        self.push_screen(HelpScreen())

    def action_about_page(self):
        self.push_screen(AboutScreen())
