# AEGIS Screen Manager Specification

AEGIS screens should follow a consistent lifecycle:

- load data
- render display
- handle input
- return state

Every screen should support:

- Up / Down
- Enter
- Esc
- Slash Search
- R Refresh
- Q Standby

Future screen modules:

aegis/screens/
- home.py
- knowledge.py
- journal.py
- inventory.py
- communications.py
- navigation.py
- hardware.py
- system.py
- search.py

The dashboard should eventually become a screen router instead of containing every screen directly.
