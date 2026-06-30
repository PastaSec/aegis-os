def render_table(rows: list[tuple[str, str]], label_width: int = 8) -> str:
    return "\n".join(f"{label:<{label_width}}{value}" for label, value in rows)

