from dataclasses import dataclass, field

from aegis.core.router import Router
from aegis.core.state import ApplicationState


@dataclass
class ApplicationContext:
    """Shared context passed through the AEGIS application shell."""

    router: Router = field(default_factory=Router)
    state: ApplicationState = field(default_factory=ApplicationState)

