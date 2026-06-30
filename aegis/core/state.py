from dataclasses import dataclass, field


@dataclass
class ApplicationState:
    selected: int = 0
    search_query: str = ""
    values: dict[str, object] = field(default_factory=dict)

