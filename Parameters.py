from pathlib import Path
from typing import List, Dict, Tuple

# Note names
LANGUAGE: str = 'spanish'  # Options: ['english', spanish']
STRING_FORMAT: str = 'spanish'  # Options: ['number', 'english', 'spanish']
SYSTEM: str = 'mixed'  # Options: ['mixed', 'sharp', 'flat']
UNICODE: bool = True

# Paths
MIDI_PATH: Path = Path('MIDI')

# MIDI parameters
BPM: int = 60
SHOW_SECONDS: bool = True
VELOCITIES_ALLOWED: List[int] = [20, 30, 40, 50, 60, 70, 80, 90]
DYNAMICS: List[str] = ["𝆏𝆏𝆏", "𝆏𝆏", "𝆏", "𝆐𝆏", "𝆐𝆑", "𝆑", "𝆑𝆑", "𝆑𝆑𝆑"]
DYNAMIC2VELOCITY: Tuple[Tuple[str, int]] = tuple(zip(DYNAMICS, VELOCITIES_ALLOWED))
VELOCITY2DYNAMIC: Tuple[Tuple[int, str]] = tuple(zip(VELOCITIES_ALLOWED, DYNAMICS))

# Signal
FS: int = 44100

# Synthesis
REVERBERATION: float = 0.3  # in seconds

# Note values
NOTE_VALUES: Dict[int, str] = {1: "𝅝", 1/2: "𝅗𝅥", 1/4: "𝅘𝅥", 1/8: "𝅘𝅥𝅮", 1/16: "𝅘𝅥𝅯", 1/32: "𝅘𝅥𝅰"}
TIE: str = " ͜ "
