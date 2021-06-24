import numpy as np
import scipy.io.wavfile as wav
import warnings as warn

from Parameters import Path, FS


warn.simplefilter("ignore", wav.WavFileWarning)


def signal_from_file(file_path: Path) -> np.ndarray:
    fs: int
    signal: np.ndarray
    fs, signal = wav.read(file_path)

    if signal.dtype == np.int16:
        signal = signal / np.iinfo(signal.dtype).max
    else:
        Exception("Signal type is not int16")

    if not len(signal.shape) == 1:
        raise Exception("Stereo not handled.")

    assert fs == FS

    return signal
