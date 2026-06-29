import shutil
import socket
import subprocess
import time

import psutil

from aegis.state import SystemState


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "n/a"


def ip_address() -> str:
    output = _run(["hostname", "-I"])
    return output.split()[0] if output and output != "n/a" else "n/a"


def temperature() -> str:
    output = _run(["vcgencmd", "measure_temp"])
    if output.startswith("temp="):
        return output.replace("temp=", "").replace("'C", "°C")
    return "n/a"


def power_status() -> str:
    raw = _run(["vcgencmd", "get_throttled"])

    if raw == "throttled=0x0":
        return "OK"

    if raw in ("throttled=0x50000", "throttled=0x50001"):
        return "Previous Undervoltage"

    if raw.startswith("throttled="):
        return raw.replace("throttled=", "WARN ")

    return "n/a"


def uptime() -> str:
    seconds = int(time.time() - psutil.boot_time())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m"


def readiness(state: SystemState) -> str:
    if state.power not in ("OK", "Previous Undervoltage"):
        return "DEGRADED"

    if state.temp != "n/a":
        try:
            temp_value = float(state.temp.replace("°C", ""))
            if temp_value >= 75:
                return "HOT"
        except ValueError:
            pass

    return "READY"


def get_system_state() -> SystemState:
    disk = shutil.disk_usage("/")
    disk_used = round((disk.used / disk.total) * 100)

    state = SystemState(
        host=socket.gethostname(),
        ip=ip_address(),
        cpu=f"{psutil.cpu_percent(interval=0.1):.0f}%",
        memory=f"{psutil.virtual_memory().percent:.0f}%",
        disk=f"{disk_used}%",
        temp=temperature(),
        power=power_status(),
        uptime=uptime(),
    )
    state.readiness = readiness(state)
    return state
