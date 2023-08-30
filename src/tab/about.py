from textual.app import ComposeResult
from textual.widgets import Label, Markdown, TabPane

ABOUT_TAB_ID = "about_tab"
ABOUT_TAB_TITLE = "About"

VERSION = "0.0.1-dev"
AUTHOR = "ricky :) (: skyzip"
YEAR = 2023

MARKDOWN_TEXT = f"""
MyPass TUI {VERSION}

Text-based user interface for MyPass.

Copyright © {YEAR} {AUTHOR}
"""


class AboutTabPane(TabPane):

    def compose(self) -> ComposeResult:
        yield Label("About MyPass TUI", classes="title")
        yield Markdown(MARKDOWN_TEXT)
