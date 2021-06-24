import numpy as np

from Samples import SamplesSet
from Objects import PieceMIDI, NoteMIDI
from Parameters import FS


def synthesize(piece: PieceMIDI, samples_set: SamplesSet) -> np.ndarray:
    piece_duration_seconds: float = piece.duration_seconds
    signal_duration_samples: int = int(FS * piece_duration_seconds)
    signal: np.ndarray = np.zeros(signal_duration_samples)

    note: NoteMIDI
    for note in piece:
        midi_number: int = note.pitch.midi_number
        velocity: int = note.velocity.midi_velocity
        note_signal: np.ndarray = samples_set.dict[(midi_number, velocity)]

        start_seconds: float = note.duration.start_seconds
        start_sample: int = int(FS * start_seconds)

        signal[start_sample: start_sample + note_signal.size] += note_signal

    return signal
