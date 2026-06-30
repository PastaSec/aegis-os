from dataclasses import dataclass
from enum import Enum


class EventType(str, Enum):
    OPEN = "open"
    BACK = "back"
    REFRESH = "refresh"
    SEARCH = "search"
    QUIT = "quit"


@dataclass(frozen=True)
class Event:
    event_type: EventType
    payload: object | None = None

