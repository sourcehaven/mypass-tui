from textual.app import App
from textual.binding import Binding
from textual.keys import Keys
from textual.widgets import Footer, TabbedContent

from .dialog.password import PasswordDialog
from .tab import *


class MyPassApp(App):
    CSS_PATH = "mypass.css"

    BINDINGS = [
        Binding(Keys.ControlC, "quit", "Quit", priority=True),
        Binding("left", "previous_tab", show=False),
        Binding("right", "next_tab", show=False),
        Binding("1", NEW_TAB_ID, NEW_TAB_TITLE),
        Binding("2", TABLE_TAB_ID, TABLE_TAB_TITLE),
        Binding("3", TREE_VIEW_TAB_ID, TREE_VIEW_TAB_TITLE),
        Binding("4", SETTINGS_TAB_ID, SETTINGS_TAB_TITLE),
        Binding("5", HELP_TAB_ID, HELP_TAB_TITLE),
        Binding("6", ABOUT_TAB_ID, ABOUT_TAB_TITLE),
        Binding("p", "password_screen", "Password screen"),
    ]

    def action_password_screen(self):
        def password_input(password: str | None) -> None:
            pass

        self.push_screen(
            PasswordDialog("Enter your master password"),
            password_input,
        )

    def compose(self):
        with TabbedContent(initial=NEW_TAB_ID):
            yield NewTabPane(NEW_TAB_TITLE, id=NEW_TAB_ID)
            yield TableViewTabPane(TABLE_TAB_TITLE, id=TABLE_TAB_ID)
            yield TreeViewTabPane(TREE_VIEW_TAB_TITLE, id=TREE_VIEW_TAB_ID)
            yield SettingsTabPane(SETTINGS_TAB_TITLE, id=SETTINGS_TAB_ID)
            yield HelpTabPane(HELP_TAB_TITLE, id=HELP_TAB_ID)
            yield AboutTabPane(ABOUT_TAB_TITLE, id=ABOUT_TAB_ID)

        yield Footer()

    def action_new_tab(self):
        self.query_one(TabbedContent).active = NEW_TAB_ID

    def action_table_view_tab(self):
        self.query_one(TabbedContent).active = TABLE_TAB_ID

    def action_tree_view_tab(self):
        self.query_one(TabbedContent).active = TREE_VIEW_TAB_ID

    def action_settings_tab(self):
        self.query_one(TabbedContent).active = SETTINGS_TAB_ID

    def action_help_tab(self):
        self.query_one(TabbedContent).active = HELP_TAB_ID

    def action_about_tab(self):
        self.query_one(TabbedContent).active = ABOUT_TAB_ID
