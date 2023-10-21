from textual.screen import Screen

from textual.binding import Binding
from textual.widgets import Footer, TabbedContent, TabPane

from ..pages import *
from ..util.session import sign_out
from ...settings import bindings


class MainScreen(Screen):
    BINDINGS = [
        Binding(bindings["vault_new"], NEW_PAGE_ID, NEW_PAGE_TITLE),
        Binding(bindings["vault_table"], TABLE_PAGE_ID, TABLE_PAGE_TITLE),
        Binding(bindings["vault_tree"], FOLDER_PAGE_ID, FOLDER_PAGE_TITLE),
        Binding("p", "password_screen", "Password screen"),
        Binding(bindings["sign_out"], "signout"),
    ]

    def compose(self):
        with TabbedContent(initial=NEW_PAGE_ID):
            with TabPane(NEW_PAGE_TITLE, id=NEW_PAGE_ID):
                yield NewEntryPage()
            with TabPane(TABLE_PAGE_TITLE, id=TABLE_PAGE_ID):
                yield TableViewPage()
            with TabPane(FOLDER_PAGE_TITLE, id=FOLDER_PAGE_ID):
                yield TreeViewPage()
        yield Footer()

    def action_new_page(self):
        self.query_one(TabbedContent).active = NEW_PAGE_ID

    def action_table_view_page(self):
        self.query_one(TabbedContent).active = TABLE_PAGE_ID

    def action_tree_view_page(self):
        self.query_one(TabbedContent).active = FOLDER_PAGE_ID

    def action_signout(self):
        sign_out(self.app)
