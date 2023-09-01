from textual.app import App
from textual.binding import Binding
from textual.keys import Keys
from textual.widgets import Footer, TabbedContent, TabPane

from .pages import *
from .screens.about import AboutScreen
from .screens.help import HelpScreen
from .screens.password import PasswordDialog
from .screens.signup import SignUpScreen


class MyPassApp(App):
    CSS_PATH = "mypass.css"

    BINDINGS = [
        Binding(Keys.ControlC, "quit", "Quit", priority=True),
        Binding("left", "previous_tab", show=False),
        Binding("right", "next_tab", show=False),
        Binding("1", NEW_PAGE_ID, NEW_PAGE_TITLE),
        Binding("2", TABLE_PAGE_ID, TABLE_PAGE_TITLE),
        Binding("3", TREE_VIEW_PAGE_ID, TREE_VIEW_PAGE_TITLE),
        Binding("4", SETTINGS_PAGE_ID, SETTINGS_PAGE_TITLE),
        Binding(Keys.F1, HELP_PAGE_ID, HELP_PAGE_TITLE),
        Binding(Keys.F2, ABOUT_PAGE_ID, ABOUT_PAGE_TITLE),
        Binding("p", "password_screen", "Password screen"),
        Binding("x", "signup_screen", "Sign Up")
    ]

    def action_password_screen(self):
        def password_input(password: str | None) -> None:
            pass

        self.push_screen(
            PasswordDialog("Enter your master password", "Password"),
            password_input,
        )

    def compose(self):
        yield from self.compose_tabs()
        yield Footer()

    def compose_tabs(self):
        with TabbedContent(initial=NEW_PAGE_ID):
            with TabPane(NEW_PAGE_TITLE, id=NEW_PAGE_ID):
                yield NewEntryPage()
            with TabPane(TABLE_PAGE_TITLE, id=TABLE_PAGE_ID):
                yield TableViewPage()
            with TabPane(TREE_VIEW_PAGE_TITLE, id=TREE_VIEW_PAGE_ID):
                yield TreeViewPage()
            with TabPane(SETTINGS_PAGE_TITLE, id=SETTINGS_PAGE_ID):
                yield SettingsPage()

    def action_new_page(self):
        self.query_one(TabbedContent).active = NEW_PAGE_ID

    def action_table_view_page(self):
        self.query_one(TabbedContent).active = TABLE_PAGE_ID

    def action_tree_view_page(self):
        self.query_one(TabbedContent).active = TREE_VIEW_PAGE_ID

    def action_settings_page(self):
        self.query_one(TabbedContent).active = SETTINGS_PAGE_ID

    def action_help_page(self):
        self.push_screen(HelpScreen())

    def action_about_page(self):
        self.push_screen(AboutScreen())

    def action_signup_screen(self):
        self.push_screen(SignUpScreen())
