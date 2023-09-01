import asyncio

from textual.widgets import Static


class Feedback(Static):

    DEFAULT_CSS = """
    Feedback {
        display: none;
        margin: 0 1;
        padding: 0 1;
        background: $boost;
    }
    """

    async def show(self, text: str, seconds: int):
        self.update(text)
        self.display = True
        await asyncio.sleep(seconds)
        self.display = False


class ErrorFeedback(Feedback):
    DEFAULT_CSS = """
    ErrorFeedback {
        background: red 40%;
    }
    """


class SuccessFeedback(Feedback):
    DEFAULT_CSS = """
    SuccessFeedback {
        background: green 40%;
    }
    """