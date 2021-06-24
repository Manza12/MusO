import numpy as np

import scipy.io.wavfile as wav

from pathlib import Path

from Midi import midi2piece
from Objects import PieceMIDI
from Samples import SamplesSet
from Synthesis import synthesize
from Parameters import FS

piece: PieceMIDI = midi2piece('prelude_543')
samples_set: SamplesSet = SamplesSet(Path('Samples/Disklavier/Samples'))

signal: np.ndarray = synthesize(piece, samples_set)
wav.write('Audio/' + piece.name + '.wav', FS, signal)
