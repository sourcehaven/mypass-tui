from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, TabbedContent, TabPane

from mypass_tui.globals import i18n, bindings
from mypass_tui.localization import KEY_FOOTER, KEY_TAB
from mypass_tui.ui.screens import (
    NEW_PAGE_ID,
    TABLE_PAGE_ID,
    FOLDER_PAGE_ID,
    NewEntryPage,
    TablePage,
    FolderPage,
)

from mypass_tui.ui.util.session import sign_out


class MainScreen(Screen):
    BINDINGS = [
        Binding(bindings["vault_new"], NEW_PAGE_ID, i18n[KEY_FOOTER]["new"]),
        Binding(bindings["vault_table"], TABLE_PAGE_ID, i18n[KEY_FOOTER]["table"]),
        Binding(bindings["vault_folder"], FOLDER_PAGE_ID, i18n[KEY_FOOTER]["folder"]),
        Binding(bindings["sign_out"], "signout"),
    ]

    def compose(self):
        with TabbedContent(initial=NEW_PAGE_ID):
            with TabPane(i18n[KEY_TAB]["new"], id=NEW_PAGE_ID):
                yield NewEntryPage()
            with TabPane(i18n[KEY_TAB]["table"], id=TABLE_PAGE_ID):
                yield TablePage()
            with TabPane(i18n[KEY_TAB]["folder"], id=FOLDER_PAGE_ID):
                yield FolderPage()
        yield Footer()

    def _set_active_tab(self, _id: str, /):
        self.query_one(TabbedContent).active = _id

    def action_new_page(self):
        self._set_active_tab(NEW_PAGE_ID)

    def action_table_page(self):
        self._set_active_tab(TABLE_PAGE_ID)

    def action_folder_page(self):
        self._set_active_tab(FOLDER_PAGE_ID)

    def action_signout(self):
        sign_out(self.app)
