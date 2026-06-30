from dataclasses import dataclass


@dataclass(frozen=True)
class FieldTheme:
    background: str = "black"
    foreground: str = "white"
    accent: str = "cyan"
    success: str = "green"
    muted: str = "dim"
    divider: str = "------------------------------"
    selected_marker: str = ">"
    unselected_marker: str = " "
    empty_menu: str = "  None found"

    def title(self, text: str) -> str:
        return f"[bold {self.accent}]{text}[/bold {self.accent}]"

    def status(self, text: str) -> str:
        return text

    def footer(self, text: str) -> str:
        return self.muted_text(text)

    def muted_text(self, text: str) -> str:
        return f"[{self.muted}]{text}[/{self.muted}]"

    def selection(self, selected: bool) -> str:
        if selected:
            return self.selected_marker
        return self.unselected_marker


FIELD_THEME = FieldTheme()
