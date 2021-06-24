import numpy as np

from math import gcd
from typing import Optional, List, Dict

from Utils import pitch_class2string, ticks2seconds
from Parameters import *


class NoteValue:

    def __init__(self, numerator: int, denominator: int):
        d = gcd(numerator, denominator)

        self.numerator: int = numerator // d
        self.denominator: int = denominator // d

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


class Velocity:

    def __init__(self, midi_velocity: int, quantization: Optional[Dict[int, str]] = VELOCITY2DYNAMIC):
        assert type(midi_velocity) == int, 'Parameter midi_velocity should be an integer.'
        assert 0 <= midi_velocity < 128, 'Parameter midi_velocity should be comprised between 0 and 128.'

        if quantization is None:
            self.quantized: bool = False
            self.value: int = midi_velocity
        else:
            assert midi_velocity in quantization, 'Parameters midi_velocity should be in ' + str(quantization.keys())

            self.quantized: bool = True
            self.value: int = midi_velocity
            self.dynamic: str = quantization[midi_velocity]

    def __str__(self):
        result: str = str(self.value)
        if self.quantized:
            result += " (" + self.dynamic + ")"
        return result


class DurationMIDI:

    def __init__(self, start_ticks: int, end_ticks: int):
        assert type(start_ticks) == int, 'Parameter start should be an integer.'
        assert type(end_ticks) == int, 'Parameter end should be an integer.'

        assert start_ticks < end_ticks, 'Parameter end should be greater than start.'

        # Values in ticks
        self.start: int = start_ticks
        self.end: int = end_ticks
        self.duration_ticks: int = end_ticks - start_ticks

        # Values in seconds
        self.start_seconds: float = ticks2seconds(self.start)
        self.end_seconds: float = ticks2seconds(self.end)
        self.duration_seconds: float = ticks2seconds(self.duration_ticks)

    def __str__(self, seconds: bool = SHOW_SECONDS):
        if seconds:
            return "[" + str(self.start_seconds) + "s" + ", " \
                   + str(self.end_seconds) + "s" + "]" + " (" \
                   + str(self.duration_seconds) + "s" + ")"
        else:
            return "[" + str(self.start) + " ticks" + ", " \
                   + str(self.end) + " ticks" + "]" + " (" \
                   + str(self.duration_ticks) + " ticks" + ")"


class Pitch:

    def __init__(self, midi_number: int):
        # Check number validity
        assert type(midi_number) == int, 'Parameter number should be an integer.'

        # Perform assignments
        self.midi_number: int = midi_number
        self.pitch_class: int = midi_number % 12
        self.octave: int = midi_number // 12 - 1

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


class NoteMIDI:

    def __init__(self, midi_number: int, start_ticks: int, end_ticks: int, midi_velocity: int,
                 quantization: Optional[Dict[int, str]] = VELOCITY2DYNAMIC):
        self.pitch = Pitch(midi_number)
        self.duration = DurationMIDI(start_ticks, end_ticks)
        self.velocity = Velocity(midi_velocity, quantization=quantization)

    def __str__(self):
        return str(self.pitch) + ", " + str(self.duration) + ", " + str(self.velocity)
