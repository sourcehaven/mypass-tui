from enum import Enum, auto


class FeedbackStyle(Enum):
    SUCCESS = auto()
    ERROR = auto()
    INFO = auto()
    NEUTRAL = auto()
    WARNING = auto()
