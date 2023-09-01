from textual.widgets import Label

from .base import BaseSideBar


class SideBar(BaseSideBar):

    def _compose(self):
        yield Label('Hello')
