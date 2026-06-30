from dataclasses import dataclass


@dataclass(frozen=True)
class FieldTheme:
    background: str = "black"
    foreground: str = "white"
    accent: str = "cyan"
    success: str = "green"
    muted: str = "dim"
    divider: str = "------------------------------"


FIELD_THEME = FieldTheme()

