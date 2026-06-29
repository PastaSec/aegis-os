from dataclasses import dataclass


@dataclass
class SystemState:
    host: str = "n/a"
    ip: str = "n/a"
    cpu: str = "n/a"
    memory: str = "n/a"
    disk: str = "n/a"
    temp: str = "n/a"
    power: str = "n/a"
    uptime: str = "n/a"
    readiness: str = "UNKNOWN"
