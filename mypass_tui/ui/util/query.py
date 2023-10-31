from textual.css.query import NoMatches
from textual.widget import Widget
from textual.widgets import TabbedContent, TabPane


def query_active_tab(screen: Widget):
    try:
        tabbed_content = screen.query_one(TabbedContent)
        active_tab = screen.query(f"#{tabbed_content.active}")[1]
        return active_tab
    except NoMatches:
        return screen


def query_tabs(screen: Widget):
    try:
        tabbed_content = screen.query_one(TabbedContent)
        tabs = tabbed_content.query(TabPane)
        return tabs
    except NoMatches:
        return screen
