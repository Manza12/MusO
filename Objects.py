from Python.Utils import pitch_class2string
from Python.Parameters import *


class Pitch:

    def __init__(self, midi_number: int):
        # Check number validity
        assert type(midi_number) == int, 'Parameter number should be an integer.'

        # Perform assignments
        self.midi_number = midi_number
        self.pitch_class = midi_number % 12
        self.octave = midi_number // 12 - 1

    def __str__(self, string_format: str = STRING_FORMAT, unicode: bool = UNICODE, system: str = SYSTEM):
        string_format_options = ['number', 'english', 'spanish']

        # Check string format validity
        assert string_format in string_format_options, \
            'Parameter string_format should be one of ' + str(string_format_options)
        assert type(unicode) == bool, 'Parameter unicode should be boolean'

        # Switch
        if string_format == 'number':
            return str(self.midi_number)
        else:
            return pitch_class2string(self.pitch_class, string_format, unicode, system) + str(self.octave)
