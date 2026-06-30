from dataclasses import dataclass


DEFAULT_DOCUMENT_HEIGHT = 13


def clamp_offset(offset: int, total_lines: int, height: int = DEFAULT_DOCUMENT_HEIGHT) -> int:
    max_offset = max(total_lines - height, 0)
    return min(max(offset, 0), max_offset)


def current_line(offset: int, total_lines: int) -> int:
    if total_lines <= 0:
        return 0
    return min(offset + 1, total_lines)


def visible_lines(lines: list[str], offset: int, height: int = DEFAULT_DOCUMENT_HEIGHT) -> list[str]:
    start = clamp_offset(offset, len(lines), height)
    return lines[start : start + height]


@dataclass
class DocumentViewState:
    offset: int = 0
    height: int = DEFAULT_DOCUMENT_HEIGHT

    def reset(self) -> None:
        self.offset = 0

    def scroll(self, amount: int, total_lines: int) -> None:
        self.offset = clamp_offset(self.offset + amount, total_lines, self.height)

    def page_up(self, total_lines: int) -> None:
        self.scroll(-self.height, total_lines)

    def page_down(self, total_lines: int) -> None:
        self.scroll(self.height, total_lines)

    def home(self) -> None:
        self.offset = 0

    def end(self, total_lines: int) -> None:
        self.offset = clamp_offset(total_lines, total_lines, self.height)

    def line_number(self, total_lines: int) -> int:
        return current_line(self.offset, total_lines)

