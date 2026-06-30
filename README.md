# AEGIS OS

**Autonomous Emergency & General Information System**

AEGIS OS is an offline-first community resilience platform built around a portable Raspberry Pi operator console. The first reference build uses a Raspberry Pi 3 Model B and an Adafruit 2.8 inch PiTFT, but the project is intended to become larger than a single cyberdeck.

The goal is simple:

> If normal infrastructure becomes unreliable, Ian and his neighbors should still have a place to connect, communicate, learn, coordinate, and share resources.

AEGIS OS is not a novelty cyberdeck, not a prepper toy, and not a laptop replacement. It is a small, practical operations platform for local knowledge, local communications, and local coordination.

## Repository

```text
PastaSec/aegis-os
```

## Project pillars

AEGIS OS is built around three operating principles:

```text
Knowledge. Communication. Resilience.
```

### Knowledge

AEGIS should preserve useful information locally:

- offline Wikipedia / ZIM libraries
- first aid and medical references
- preparedness and safety documents
- networking and Linux documentation
- local maps and procedures
- personal SOPs and project notes
- community guides and resource lists

### Communication

AEGIS should help people coordinate locally even when the Internet is unavailable:

- local Wi-Fi access point
- community portal
- announcements
- message board
- resource requests
- file sharing
- future mesh support
- future LoRa / radio integration where legal and appropriate

### Resilience

AEGIS should continue to work when normal services fail:

- offline-first design
- local authentication
- local storage
- local logs
- modular hardware support
- graceful degradation
- no hard dependency on cloud APIs

## Current reference hardware

The first AEGIS Console currently consists of:

- Raspberry Pi 3 Model B Rev 1.2
- Debian GNU/Linux 13 Trixie, 64-bit aarch64
- Adafruit 2.8 inch PiTFT resistive touchscreen
- ILI9341 / fb_ili9340 display framebuffer on `/dev/fb1`
- STMPE610 touch controller detected over SPI
- Wi-Fi and Bluetooth onboard
- SSH enabled
- terminal console mapped to the PiTFT using systemd

## Development architecture

Sprint 001 organizes the terminal application into:

- `aegis/core/` for routing, events, screen contracts, and shared application state
- `aegis/screens/` for Capability screen rendering
- `aegis/widgets/` for reusable terminal UI helpers
- `aegis/themes/` for visual constants
- `aegis/models/` for shared data shapes

`aegis/dashboard.py` remains a compatibility shell exposing `run_dashboard()`.
The `aegis` console command and appliance startup continue to enter through that stable surface.

On Windows development systems, Raspberry Pi-specific Hardware fields may show `n/a`.
Those fields depend on Pi tools and devices that are present on the appliance, not on a Windows workstation.

## Product model

AEGIS is organized as three related systems.

### AEGIS Console

The handheld operator interface. This is the cyberdeck itself.

Primary functions:

- boot to readable terminal dashboard
- monitor local system health
- launch network tools
- access offline docs
- manage the community portal
- connect to expansion modules
- SSH into trusted systems

### AEGIS Hub

The local infrastructure node. This may run on the same Raspberry Pi, a larger home server, or another dedicated device.

Primary functions:

- local community web portal
- document server
- search service
- bulletin board
- resource inventory
- local chat or message exchange
- node monitoring

### AEGIS Nodes

Small deployable devices that extend reach or gather data.

Possible node types:

- Raspberry Pi Zero W / Zero 2 W receivers
- ESP32 sensor/status nodes
- OpenWrt routers
- future LoRa nodes
- USB serial devices
- Flipper Zero as a dockable instrument

## Flipper Zero role

The Flipper Zero is treated as a dockable expansion instrument, not as the main computer.

When plugged in over USB, the AEGIS Console should eventually detect it as a peripheral and expose supported workflows such as serial access, file transfer, logging, and lawful radio/RFID/IR-related utility functions.

## Roadmap

### Phase 0: Hardware foundation

- [x] Boot Raspberry Pi OS / Debian Trixie
- [x] Enable SSH
- [x] Enable Wi-Fi
- [x] Enable SPI
- [x] Configure PiTFT overlay
- [x] Confirm `/dev/fb1`
- [x] Map console to PiTFT on boot

### Phase 1: Core console

- [ ] Create terminal dashboard
- [ ] Add system health monitor
- [ ] Add power/throttling monitor
- [ ] Add keyboard-first menu
- [ ] Add safe shutdown workflow
- [ ] Keep SSH and HDMI fallback intact

### Phase 2: Offline knowledge

- [ ] Define document library layout
- [ ] Add PDF/text/Markdown viewer
- [ ] Add Kiwix/ZIM support
- [ ] Add unified search
- [ ] Add curated survival, medical, and technical docs

### Phase 3: Community portal

- [ ] Local web server
- [ ] Captive-style landing page
- [ ] Announcements
- [ ] Message board
- [ ] Resource requests
- [ ] Shared files
- [ ] Local authentication

### Phase 4: Monitoring

- [ ] Pi system monitor
- [ ] Services monitor
- [ ] Network monitor
- [ ] AEGIS node monitor
- [ ] Optional home lab monitor
- [ ] Optional sensor monitor

### Phase 5: Expansion

- [ ] Flipper Zero detection
- [ ] ESP32 sensor node support
- [ ] USB serial tools
- [ ] GPS support
- [ ] OpenWrt / mesh experiments
- [ ] LoRa experiments where legal

## Non-goals

AEGIS OS should not become:

- a desktop replacement
- a general media center
- a cloud-first application
- a hacking toolkit for unauthorized activity
- a fragile pile of unrelated scripts

## Guiding question

Before adding a feature, ask:

> Does this improve knowledge, communication, coordination, or operational awareness for Ian and his community?

If yes, it belongs in AEGIS. If not, it can wait.

## Current status

AEGIS OS is in early foundation stage. The hardware display path is working, and the project is ready for software scaffolding.

The deck is the interface.  
The hub is the infrastructure.  
The nodes are the reach.  
The library is the memory.  
The portal is the meeting place.  
The community is the mission.
