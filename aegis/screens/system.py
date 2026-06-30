from aegis.widgets.frame import render_frame


def render_system_screen() -> str:
    body = (
        "AEGIS OS v0.3.0-alpha\n"
        "Mode: Field Terminal\n\n"
        "Update, backup, restore,\n"
        "logs, and configuration\n"
        "will live here."
    )
    return render_frame("System", "Maintenance", body)
