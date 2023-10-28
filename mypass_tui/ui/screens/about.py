from mypass_tui.globals import i18n
from mypass_tui.localization import fill_placeholders
from mypass_tui.ui.screens import SecondaryScreen

from textual.app import ComposeResult
from textual.widgets import Label, Markdown, Static

ABOUT_PAGE_ID = "about_page"

VERSION = "0.0.1-dev"
AUTHOR = "ricky :) (: skyzip"
YEAR = 2023


class AboutPage(Static):
    def compose(self) -> ComposeResult:
        yield Label(i18n["title"]["about"], classes="title")
        yield Markdown(fill_placeholders(i18n["about"], VERSION, YEAR, AUTHOR))


class AboutScreen(SecondaryScreen):
    def _compose(self) -> ComposeResult:
        yield AboutPage()
