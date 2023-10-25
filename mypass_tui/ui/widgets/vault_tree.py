from typing import Iterable

from textual.widgets import Tree

from mypass_tui import session
from mypass_tui.localization import i18n
from mypass_tui.model.vault_entry import TITLE, VaultEntry, append_tree

OPEN_FOLDER = "📂 "
CLOSED_FOLDER = "📁 "
FILE = "📄 "


def build_tree(tree_data, tree_widget: Tree):
    for branch in tree_data:
        if isinstance(branch, tuple):
            subtree_widget = tree_widget.root.add(CLOSED_FOLDER + branch[0])

            for e in branch[1]:
                if isinstance(e, VaultEntry):
                    subtree_widget.add_leaf(FILE + e.title, data=e)

            build_tree(branch, subtree_widget)


class VaultTree(Tree):
    def __init__(self, entries: Iterable[VaultEntry]):
        super().__init__(f".{OPEN_FOLDER}")
        self.entries = entries
        self.root.expand()

        self.tree_structure = []
        for entry in entries:
            append_tree(self.tree_structure, entry)

        build_tree(self.tree_structure, self)

    def add_entry(self, entry: VaultEntry):
        append_tree(self.tree_structure, entry)
        build_tree([entry], self)

    def on_tree_node_collapsed(self, collapsed: Tree.NodeCollapsed):
        node = collapsed.node
        node.set_label(node.label.plain.replace(OPEN_FOLDER, CLOSED_FOLDER))

    def on_tree_node_expanded(self, expanded: Tree.NodeExpanded):
        node = expanded.node
        node.set_label(node.label.plain.replace(CLOSED_FOLDER, OPEN_FOLDER))

    def on_tree_node_selected(self, selected: Tree.NodeSelected):
        from mypass_tui.ui.screens import InputScreen

        node = selected.node

        def callback(fields):
            if fields:
                session.user.vault_update(id=node.data.id, fields=fields)
                node.set_label(FILE + fields[TITLE])
                node.data.update(fields)

        if isinstance(node.data, VaultEntry):
            self.app.push_screen(
                InputScreen(title=i18n.title__edit, inputs=node.data.input_details()),
                callback=callback,
            )
