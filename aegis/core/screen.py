from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from aegis.core.events import Event


class ScreenResultType(str, Enum):
    NONE = "none"
    ROUTE = "route"
    BACK = "back"
    QUIT = "quit"


@dataclass(frozen=True)
class ScreenResult:
    result_type: ScreenResultType = ScreenResultType.NONE
    route: str | None = None


class Screen(Protocol):
    def load(self) -> None:
        ...

    def render(self, selected: int = 0) -> str:
        ...

    def handle_input(self, event: Event) -> ScreenResult:
        ...

