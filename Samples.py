import os

import numpy as np

from pathlib import Path
from typing import Dict, Tuple, List

from IO import signal_from_file, wav
from Objects import PieceMIDI, NoteMIDI
from Midi import midi2piece
from Parameters import FS


class SamplesSet:

    def __init__(self, samples_folder: Path):
        files: List[str] = os.listdir(samples_folder)
        self.dict: Dict[Tuple[int, int], np.ndarray] = {}

        for file in files:
            sample = signal_from_file(samples_folder / Path(file))
            radix = file.split('.')[0]
            parameters = radix.split('_')
            assert len(parameters) == 2
            try:
                pitch: int = int(parameters[0])
                velocity: int = int(parameters[1])
                self.dict[(pitch, velocity)] = sample
            except ValueError:
                raise Exception('File with bad form present in folder: %r' % file)


def split_samples(midi_file_name: str, midi_folder_path: Path,
                  wav_file_name: str, wav_folder_path: Path,
                  samples_folder: Path):
    samples_piece: PieceMIDI = midi2piece(midi_file_name, midi_folder_path)
    samples_wav: np.ndarray
    samples_wav = signal_from_file(Path(wav_folder_path) / Path(wav_file_name + '.wav'))

    note: NoteMIDI
    for note in samples_piece:
        start_seconds: float = note.duration.start_seconds
        end_seconds: float = note.duration.end_seconds
        start_sample: int = int(start_seconds * FS)
        end_sample: int = int(end_seconds * FS)
        sample_wav: np.ndarray = samples_wav[start_sample:end_sample]

        number: int = note.pitch.midi_number
        velocity: int = note.velocity.midi_velocity

        wav.write(samples_folder / Path(str(number) + "_" + str(velocity) + ".wav"), FS, sample_wav)


if __name__ == '__main__':
    name: str = 'grid'
    folder: Path = Path('Samples/Disklavier')
    split_samples(name, folder, name, folder, folder / Path('Samples'))
