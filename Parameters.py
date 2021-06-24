from pathlib import Path
from typing import List, Dict

# Note names
LANGUAGE: str = 'spanish'  # Options: ['english', spanish']
STRING_FORMAT: str = 'spanish'  # Options: ['number', 'english', 'spanish']
SYSTEM: str = 'mixed'  # Options: ['mixed', 'sharp', 'flat']
UNICODE: bool = True

# Paths
MIDI_PATH: Path = Path('MIDI')

# MIDI parameters
TICKS_PER_BEAT: int = 960
BPM: int = 60
SHOW_SECONDS: bool = True
VELOCITIES_ALLOWED: List[int] = [20, 30, 40, 50, 60, 70, 80, 90]
DYNAMICS: List[str] = ["𝆏𝆏𝆏", "𝆏𝆏", "𝆏", "𝆐𝆏", "𝆐𝆑", "𝆑", "𝆑𝆑", "𝆑𝆑𝆑"]
DYNAMIC2VELOCITY: Dict[str, int] = {DYNAMICS[i]: VELOCITIES_ALLOWED[i] for i in range(len(DYNAMICS))}
VELOCITY2DYNAMIC: Dict[int, str] = {VELOCITIES_ALLOWED[i]: DYNAMICS[i] for i in range(len(VELOCITIES_ALLOWED))}

# Signal
FS: int = 44100

# Note values
NOTE_VALUES: Dict[int, str] = {1: "𝅝", 1/2: "𝅗𝅥", 1/4: "𝅘𝅥", 1/8: "𝅘𝅥𝅮", 1/16: "𝅘𝅥𝅯", 1/32: "𝅘𝅥𝅰"}
TIE: str = " ͜ "
