import numpy as np

from math import gcd

from Utils import pitch_class2string
from Parameters import *


class NoteValue:

    def __init__(self, numerator: int, denominator: int):
        d = gcd(numerator, denominator)

        self.numerator = numerator // d
        self.denominator = denominator // d

    def __str__(self):
        if 1 / self.denominator in NOTE_VALUES.keys():
            appendix = ""
            a = self.denominator
            a_exp = int(np.log2(a))
        else:
            a_exp = int(np.log2(self.denominator))
            a = 2 ** a_exp
            b = self.denominator

            d = gcd(a, b)

            nv = NOTE_VALUES[1 / a]

            appendix = "[" + str(b // d) + ":" + str(a // d) + nv + "]"

        radix = ""
        num_bin = bin(self.numerator)
        num_bin = num_bin[2:]
        n = len(num_bin)
        for i in range(n):
            if num_bin[i] == '1':
                key = 2**(n - i - 1 - a_exp)
                if key <= 1:
                    radix += NOTE_VALUES[key] + TIE
                else:
                    for j in range(key):
                        radix += NOTE_VALUES[1] + TIE
        radix = radix[:-2]

        result = radix + appendix

        return result


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
