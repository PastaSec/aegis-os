from aegis.state import SystemState
from aegis.widgets.frame import render_frame


def render_hardware_screen(state: SystemState) -> str:
    body = (
        f"Host    {state.host}\n"
        f"IP      {state.ip}\n"
        f"CPU     {state.cpu}\n"
        f"RAM     {state.memory}\n"
        f"Disk    {state.disk}\n"
        f"Temp    {state.temp}\n"
        f"Power   {state.power}\n"
        f"Uptime  {state.uptime}"
    )
    return render_frame("Hardware", "System Diagnostics", body)

