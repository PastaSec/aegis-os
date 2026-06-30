from pathlib import Path

FB = Path("/dev/fb1")
FB.write_bytes(b"\x00" * (320 * 240 * 2))
