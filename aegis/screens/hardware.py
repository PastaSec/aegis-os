from aegis.state import SystemState
from aegis.widgets.frame import render_frame
from aegis.widgets.table import render_table


def render_hardware_screen(state: SystemState) -> str:
    body = render_table(
        [
            ("Host", state.host),
            ("IP", state.ip),
            ("CPU", state.cpu),
            ("RAM", state.memory),
            ("Disk", state.disk),
            ("Temp", state.temp),
            ("Power", state.power),
            ("Uptime", state.uptime),
        ]
    )
    return render_frame("Hardware", "System Diagnostics", body)
