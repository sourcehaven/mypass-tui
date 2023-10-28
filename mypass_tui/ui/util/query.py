from textual.css.query import NoMatches
from textual.widget import Widget
from textual.widgets import TabbedContent


def query_active_tab(screen: Widget):
    try:
        tabbed_content = screen.query_one(TabbedContent)
        active_tab = screen.query(f"#{tabbed_content.active}")[1]
        return active_tab
    except NoMatches:
        return screen
