from Objects import NoteValue
import sys

num = int(sys.argv[1])
den = int(sys.argv[2])

note_value = NoteValue(num, den)
print(note_value)
