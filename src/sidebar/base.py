from abc import abstractmethod

from textual.app import ComposeResult
from textual.containers import Container


class BaseSideBar(Container):

    @abstractmethod
    def _compose(self):
        pass

    def compose(self) -> ComposeResult:
        yield Container(*self._compose(), id="sidebar")
