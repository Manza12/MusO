# Note names
LANGUAGE = 'spanish'  # Options: ['english', spanish']
STRING_FORMAT = 'spanish'  # Options: ['number', 'english', 'spanish']
SYSTEM = 'mixed'  # Options: ['mixed', 'sharp', 'flat']
UNICODE = True

# MIDI parameters
TICKS_PER_BEAT = 960
BPM = 60
SHOW_SECONDS = True
VELOCITIES_ALLOWED = [20, 30, 40, 50, 60, 70, 80, 90]
DYNAMICS = ["𝆏𝆏𝆏", "𝆏𝆏", "𝆏", "𝆐𝆏", "𝆐𝆑", "𝆑", "𝆑𝆑", "𝆑𝆑𝆑"]
DYNAMIC2VELOCITY = {DYNAMICS[i]: VELOCITIES_ALLOWED[i] for i in range(len(DYNAMICS))}
VELOCITY2DYNAMIC = {VELOCITIES_ALLOWED[i]: DYNAMICS[i] for i in range(len(VELOCITIES_ALLOWED))}

# Note values
NOTE_VALUES = {1: "𝅝", 1/2: "𝅗𝅥", 1/4: "𝅘𝅥", 1/8: "𝅘𝅥𝅮", 1/16: "𝅘𝅥𝅯", 1/32: "𝅘𝅥𝅰"}
TIE = " ͜ "
