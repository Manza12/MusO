from Objects import NoteValue
import sys

num: int = int(sys.argv[1])
den: int = int(sys.argv[2])

note_value: NoteValue = NoteValue(num, den)
print(note_value)
