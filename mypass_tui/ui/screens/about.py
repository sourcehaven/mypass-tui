from mypass_tui.globals import i18n
from mypass_tui.localization import fill_placeholders, KEY_TITLE
from mypass_tui.ui.screens import SecondaryScreen

from textual.app import ComposeResult
from textual.widgets import Label, Markdown, Static

ABOUT_PAGE_ID = "about_page"

VERSION = "0.0.1-dev"
AUTHOR = "ricky :) (: skyzip"
YEAR = 2023


class AboutPage(Static):
    def compose(self) -> ComposeResult:
        yield Label(i18n[KEY_TITLE]["about"], classes="title")
        yield Label(fill_placeholders(i18n["about"], VERSION, YEAR, AUTHOR), classes="multiline")


class AboutScreen(SecondaryScreen):
    def _compose(self) -> ComposeResult:
        yield AboutPage()
