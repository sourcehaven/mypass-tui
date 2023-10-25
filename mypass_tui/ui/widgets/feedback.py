from typing import Type

from textual.css.query import QueryType
from textual.dom import DOMNode
from textual.widgets import Static

from mypass_tui.model import FeedbackStyle


class Feedback(Static):
    DEFAULT_DISPLAY_SECONDS = 3.0
    DEFAULT_ANIMATION_SECONDS = 0.5

    def on_mount(self) -> None:
        if self.renderable != "":
            self.styles.display = "block"

    def set_style(self, style: FeedbackStyle):
        def set_feedback_class(class_name):
            self.remove_class(
                "neutral_feedback", "info_feedback", "error_feedback", "warning_feedback", "success_feedback"
            )
            self.add_class(class_name)
            self.border_title = class_name.split("_")[0].capitalize()

        match style:
            case FeedbackStyle.NEUTRAL:
                set_feedback_class("neutral_feedback")
            case FeedbackStyle.INFO:
                set_feedback_class("info_feedback")
            case FeedbackStyle.ERROR:
                set_feedback_class("error_feedback")
            case FeedbackStyle.WARNING:
                set_feedback_class("warning_feedback")
            case FeedbackStyle.SUCCESS:
                set_feedback_class("success_feedback")

    @classmethod
    def _show(
        cls,
        node: DOMNode,
        text: str,
        style: FeedbackStyle,
        selector: str | Type[QueryType] = None,
        offset=(0.0, -3.0),
        display_seconds: int = DEFAULT_DISPLAY_SECONDS,
        animation_seconds: int = DEFAULT_ANIMATION_SECONDS,
    ):
        if selector is None:
            selector = cls
        if display_seconds is None:
            display_seconds = Feedback.DEFAULT_DISPLAY_SECONDS
        if animation_seconds is None:
            animation_seconds = Feedback.DEFAULT_ANIMATION_SECONDS

        obj = node.query_one(selector, cls)
        obj.set_style(style)
        obj.update(text)
        obj.styles.offset = offset
        obj.styles.opacity = 0.0

        def hide_on_complete():
            def hide_display():
                obj.display = False

            obj.styles.animate(
                "opacity", value=0.0, duration=animation_seconds, delay=display_seconds, on_complete=hide_display
            )

        obj.display = True
        obj.styles.animate("opacity", value=1.0, duration=animation_seconds, on_complete=hide_on_complete)

    @classmethod
    def info(
        cls,
        node: DOMNode,
        text: str,
        selector: str | Type[QueryType] = None,
        offset=(0.0, -3.0),
        display_seconds: int = DEFAULT_DISPLAY_SECONDS,
        animation_seconds: int = DEFAULT_ANIMATION_SECONDS,
    ):
        Feedback._show(
            node=node,
            text=text,
            selector=selector,
            style=FeedbackStyle.INFO,
            offset=offset,
            display_seconds=display_seconds,
            animation_seconds=animation_seconds,
        )

    @classmethod
    def error(
        cls,
        node: DOMNode,
        text: str,
        selector: str | Type[QueryType] = None,
        offset=(0.0, -3.0),
        display_seconds: int = DEFAULT_DISPLAY_SECONDS,
        animation_seconds: int = DEFAULT_ANIMATION_SECONDS,
    ):
        Feedback._show(
            node=node,
            text=text,
            selector=selector,
            style=FeedbackStyle.ERROR,
            offset=offset,
            display_seconds=display_seconds,
            animation_seconds=animation_seconds,
        )

    @classmethod
    def warning(
        cls,
        node: DOMNode,
        text: str,
        selector: str | Type[QueryType] = None,
        offset=(0.0, -3.0),
        display_seconds: int = DEFAULT_DISPLAY_SECONDS,
        animation_seconds: int = DEFAULT_ANIMATION_SECONDS,
    ):
        Feedback._show(
            node=node,
            text=text,
            selector=selector,
            style=FeedbackStyle.WARNING,
            offset=offset,
            display_seconds=display_seconds,
            animation_seconds=animation_seconds,
        )

    @classmethod
    def neutral(
        cls,
        node: DOMNode,
        text: str,
        selector: str | Type[QueryType] = None,
        offset=(0.0, -3.0),
        display_seconds: int = DEFAULT_DISPLAY_SECONDS,
        animation_seconds: int = DEFAULT_ANIMATION_SECONDS,
    ):
        Feedback._show(
            node=node,
            text=text,
            selector=selector,
            style=FeedbackStyle.NEUTRAL,
            offset=offset,
            display_seconds=display_seconds,
            animation_seconds=animation_seconds,
        )

    @classmethod
    def success(
        cls,
        node: DOMNode,
        text: str,
        selector: str | Type[QueryType] = None,
        offset=(0.0, -3.0),
        display_seconds: int = DEFAULT_DISPLAY_SECONDS,
        animation_seconds: int = DEFAULT_ANIMATION_SECONDS,
    ):
        Feedback._show(
            node=node,
            text=text,
            selector=selector,
            style=FeedbackStyle.SUCCESS,
            offset=offset,
            display_seconds=display_seconds,
            animation_seconds=animation_seconds,
        )

    @staticmethod
    def on_error(
        *exc: Type[Exception],
        selector: str | Type[QueryType] = None,
        display_seconds: int = DEFAULT_DISPLAY_SECONDS,
        animation_seconds: int = DEFAULT_ANIMATION_SECONDS,
    ):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                try:
                    return func(self, *args, **kwargs)
                except exc as e:
                    Feedback.error(
                        node=self,
                        text=str(e),
                        selector=selector,
                        display_seconds=display_seconds,
                        animation_seconds=animation_seconds,
                    )

            return wrapper

        return decorator
