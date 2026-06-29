# AEGIS OS Project Context

AEGIS OS is the Autonomous Emergency & General Information System.

Repository:
PastaSec/aegis-os

Primary mission:
Build a self-contained community resilience platform that can preserve knowledge,
enable local communication, monitor available systems, and coordinate neighbors
when normal infrastructure is unavailable or unreliable.

Core principles:
1. Offline-first.
2. Community-focused.
3. Modular architecture.
4. Observable systems.
5. Recoverable configuration.
6. No cloud dependency for core emergency functionality.
7. Claude Code is a development assistant only, not a runtime dependency.

Reference hardware:
- Raspberry Pi 3 Model B Rev 1.2
- Debian 13 Trixie, arm64
- Adafruit 2.8 inch PiTFT resistive touch display
- ILI9341 display controller
- STMPE610 touch controller
- PiTFT framebuffer at /dev/fb1
- Console mapped persistently with pitft-console.service
- Bluetooth keyboard
- Wi-Fi
- Future modules: Flipper Zero over USB, ESP32 sensor nodes, local web portal,
  offline docs, mesh/network tools, battery monitoring.

Product model:
- AEGIS Console: operator interface on the cyberdeck.
- AEGIS Hub: local community services, docs, portal, messaging, and monitoring.
- AEGIS Nodes: portable extension nodes such as ESP32, Pi Zero, OpenWrt routers,
  LoRa modules, or sensors.

Do not design AEGIS as a normal desktop application.
Do not require Internet for core features.
Do not assume a large display.
Do not hardcode modules.
Prefer simple terminal-first interfaces, local files, SQLite, systemd services,
and plain-text configuration.

Initial MVP:
Power on -> PiTFT console/dashboard -> Wi-Fi available -> offline docs usable ->
local portal available -> notes/logs work -> safe shutdown works.

