from textual.app import ComposeResult
from textual.widgets import Tree, Static

from ..widgets.input_prompt import InputPrompt

TREE_VIEW_PAGE_ID = "tree_view_page"
TREE_VIEW_PAGE_TITLE = "Tree view"


class TreeViewPage(Static):
    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree("Folder", id='tree')
        characters = tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")
        yield tree
        yield InputPrompt("tree_prompt")
