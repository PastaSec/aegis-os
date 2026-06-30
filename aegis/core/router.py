from dataclasses import dataclass, field


@dataclass(frozen=True)
class Route:
    name: str
    selected: int = 0


@dataclass
class Router:
    current: Route = field(default_factory=lambda: Route("home"))
    history: list[Route] = field(default_factory=list)

    @property
    def route_name(self) -> str:
        return self.current.name

    def go(self, name: str, selected: int = 0, current_selected: int | None = None) -> Route:
        previous_selected = self.current.selected if current_selected is None else current_selected
        self.history.append(Route(self.current.name, previous_selected))
        self.current = Route(name=name, selected=selected)
        return self.current

    def replace(self, name: str, selected: int = 0) -> Route:
        self.current = Route(name=name, selected=selected)
        return self.current

    def back(self) -> Route:
        if self.history:
            self.current = self.history.pop()
        else:
            self.current = Route("home")
        return self.current

    def reset(self) -> None:
        self.history.clear()
        self.current = Route("home")
