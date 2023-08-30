from textual.app import ComposeResult
from textual.widgets import TabPane, Tree

from ..widgets.input_prompt import InputPrompt

TREE_VIEW_TAB_ID = "tree_view_tab"
TREE_VIEW_TAB_TITLE = "Tree view"


class TreeViewTabPane(TabPane):
    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree("Dune")
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")
        yield tree
        yield InputPrompt()
