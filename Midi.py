import pathlib

import mido as mid

from Parameters import *
from Objects import NoteMIDI, PieceMIDI
from Utils import round_to_list


def print_messages(midi: mid.MidiFile):
    for i, track in enumerate(midi.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)


def check_pedal(midi: mid.MidiFile) -> bool:
    for msg in midi.tracks[0]:
        if msg.type == 'control_change':
            if msg.control == 64:
                return True
            else:
                raise NotImplementedError("Pedal not implemented yet")
    return False


def midi2piece(file_name: str) -> PieceMIDI:
    piece: PieceMIDI = PieceMIDI(file_name)
    file_path: pathlib.Path = MIDI_PATH / Path(file_name + '.mid')
    midi: mid.MidiFile = mid.MidiFile(file_path)

    has_pedal: bool = check_pedal(midi)

    if not has_pedal:
        time_ticks: int = 0
        for m, msg in enumerate(midi.tracks[0]):
            time_ticks += msg.time
            if msg.type == 'note_on':
                if msg.velocity != 0:
                    m_end: int = m + 1
                    delta_ticks: int = 0
                    while True:
                        delta_ticks += midi.tracks[0][m_end].time
                        if midi.tracks[0][m_end].note == msg.note and midi.tracks[0][m_end].velocity == 0:
                            velocity: int = round_to_list(msg.velocity, VELOCITIES_ALLOWED)
                            note: NoteMIDI = NoteMIDI(msg.note, time_ticks, time_ticks + delta_ticks, velocity)
                            piece.append(note)
                            break
                        m_end += 1
    else:
        raise NotImplementedError("Pedal not implemented yet")

    return piece
