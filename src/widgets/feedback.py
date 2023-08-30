import asyncio

from textual.widgets import Static


class Feedback(Static):
    async def show(self, text: str, seconds: int):
        self.update(text)
        self.display = True
        await asyncio.sleep(seconds)
        self.display = False


class ErrorFeedback(Feedback):
    pass


class SuccessFeedback(Feedback):
    pass
