from textual.screen import Screen

from textual.binding import Binding
from textual.widgets import Footer, TabbedContent, TabPane

from mypass_tui.localization import i18n
from mypass_tui.settings import bindings
from mypass_tui.ui.pages import *
from mypass_tui.ui.util.session import sign_out


class MainScreen(Screen):
    BINDINGS = [
        Binding(bindings["vault_new"], NEW_PAGE_ID, i18n.footer__new),
        Binding(bindings["vault_table"], TABLE_PAGE_ID, i18n.footer__table),
        Binding(bindings["vault_tree"], FOLDER_PAGE_ID, i18n.footer__folder),
        # Binding(bindings["vault_tile"], TILE_PAGE_ID, i18n.footer__tile),
        Binding("p", "password_screen", "Password screen"),
        Binding(bindings["sign_out"], "signout"),
    ]

    def compose(self):
        with TabbedContent(initial=NEW_PAGE_ID):
            with TabPane(i18n.tab__new, id=NEW_PAGE_ID):
                yield NewEntryPage()
            with TabPane(i18n.tab__table, id=TABLE_PAGE_ID):
                yield TablePage()
            with TabPane(i18n.tab__folder, id=FOLDER_PAGE_ID):
                yield FolderPage()
            with TabPane(i18n.tab__tile, id=TILE_PAGE_ID):
                yield TilePage()
        yield Footer()

    def action_new_page(self):
        self.query_one(TabbedContent).active = NEW_PAGE_ID

    def action_table_view_page(self):
        self.query_one(TabbedContent).active = TABLE_PAGE_ID

    def action_tree_view_page(self):
        self.query_one(TabbedContent).active = FOLDER_PAGE_ID

    def action_signout(self):
        sign_out(self.app)
