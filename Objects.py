from __future__ import annotations

import numpy as np
import collections.abc as abc

from math import gcd
from typing import Optional, List, Dict

from Utils import pitch_class2string, ticks2seconds, seconds2ticks
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
            self.midi_velocity: int = midi_velocity
        else:
            assert midi_velocity in quantization, 'Parameters midi_velocity should be in ' + str(quantization.keys())

            self.quantized: bool = True
            self.midi_velocity: int = midi_velocity
            self.dynamic: str = quantization[midi_velocity]

    def __str__(self):
        result: str = str(self.midi_velocity)
        if self.quantized:
            result += " (" + self.dynamic + ")"
        return result


class DurationMIDI:

    def __init__(self, start_ticks: int, end_ticks: int):
        assert type(start_ticks) == int, 'Parameter start should be an integer.'
        assert type(end_ticks) == int, 'Parameter end should be an integer.'

        assert start_ticks < end_ticks, 'Parameter end should be greater than start.'

        # Values in ticks
        self.start_ticks: int = start_ticks
        self.end_ticks: int = end_ticks
        self.duration_ticks: int = end_ticks - start_ticks

        # Values in seconds
        self.start_seconds: float = ticks2seconds(self.start_ticks)
        self.end_seconds: float = ticks2seconds(self.end_ticks)
        self.duration_seconds: float = ticks2seconds(self.duration_ticks)

    def __str__(self, seconds: bool = SHOW_SECONDS):
        if seconds:
            return "[" + str(self.start_seconds) + "s" + ", " \
                   + str(self.end_seconds) + "s" + "]" + " (" \
                   + str(self.duration_seconds) + "s" + ")"
        else:
            return "[" + str(self.start_ticks) + " ticks" + ", " \
                   + str(self.end_ticks) + " ticks" + "]" + " (" \
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


class PieceMIDI(abc.MutableSequence[NoteMIDI]):
    def __init__(self, name: str = None):
        self.name: str = name
        self.duration_ticks: int = 0
        self.duration_seconds: float = 0.0
        self.notes: List[NoteMIDI] = list()

    def insert(self, index: int, note: NoteMIDI) -> None:
        # Check + Update
        self.check_update(note)

        # Insert
        self.notes.insert(index, note)

    def append(self, note: NoteMIDI) -> None:
        # Check + Update
        self.check_update(note)

        # Append
        self.notes.append(note)

    def __len__(self) -> int:
        return len(self.notes)

    def __delitem__(self, index: int) -> None:
        self.notes.__delitem__(index)

    def __setitem__(self, index: int, note: NoteMIDI) -> None:
        # Check + Update
        self.check_update(note)

        # Set item
        self.notes.__setitem__(index, note)

    def __getitem__(self, index: int) -> NoteMIDI:
        return self.notes.__getitem__(index)

    def sub_piece_ticks(self, start_ticks: int, end_ticks: int) -> PieceMIDI:
        new_piece = PieceMIDI(name=self.name + "(from " + str(start_ticks) + " ticks to " + str(end_ticks) + " ticks )")
        for note in self:
            if start_ticks <= note.duration.start_ticks <= end_ticks:
                new_note = NoteMIDI(note.pitch.midi_number,
                                    note.duration.start_ticks - start_ticks, note.duration.end_ticks - start_ticks,
                                    note.velocity.midi_velocity)
                new_piece.append(new_note)
        return new_piece

    def sub_piece_seconds(self, start_seconds: float, end_seconds: float) -> PieceMIDI:
        start_ticks: int = seconds2ticks(start_seconds)
        end_ticks: int = seconds2ticks(end_seconds)
        new_piece: PieceMIDI = self.sub_piece_ticks(start_ticks, end_ticks)
        return new_piece

    def __str__(self) -> str:
        result = ""
        result += "Piece: "

        if self.name:
            result += self.name + "\n"
        else:
            result += "[no name]\n"

        result += "Notes:\n"
        for i in range(len(self)):
            result += self[i].__str__() + "\n"

        return result

    def check_update(self, note: NoteMIDI):
        # Check type
        if not type(note) is NoteMIDI:
            raise TypeError("%r should be a Note" % note)

        # Update length
        if note.duration.end_seconds > self.duration_ticks:
            self.duration_ticks = note.duration.end_ticks
            self.duration_seconds = ticks2seconds(self.duration_ticks)
