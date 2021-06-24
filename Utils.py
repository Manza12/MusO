import numpy as np

from typing import List

from Parameters import *


def ticks2seconds(ticks: int) -> float:
    seconds: float = ((ticks / TICKS_PER_BEAT) / (BPM / 60))
    return seconds


def seconds2ticks(seconds: float) -> int:
    ticks: int = round(TICKS_PER_BEAT * BPM * seconds / 60)
    return ticks


def round_to_list(value: int, list_values: List[int]) -> int:
    diffs: np.ndarray = np.abs(np.array(value, dtype=np.int16) - np.array(list_values, dtype=np.int16))
    index = np.argmin(diffs)
    rounded_value: int = list_values[index]
    return rounded_value


def pitch_class2string(pitch_class: int, language: str = LANGUAGE, unicode: bool = True, system: str = 'mixed'):
    pitch_class = pitch_class % 12
    language_options = ['english', 'spanish']
    system_options = ['mixed', 'sharp', 'flat']

    # Check parameter types
    assert type(pitch_class) == int, 'Parameter pitch_class should be an integer.'
    assert type(language) == str, 'Parameter language should be a string.'
    assert type(unicode) == bool, 'Parameter unicode should be a boolean.'
    assert type(system) == str, 'Parameter system should be a string.'

    # Check parameter validity
    assert language in language_options, 'Parameter language should be one of ' + str(language_options)
    assert system in system_options, 'Parameter system should be one of ' + str(system_options)

    # Language switch
    if language == 'english':
        do = 'C'
        re = 'D'
        mi = 'E'
        fa = 'F'
        sol = 'G'
        la = 'A'
        si = 'B'
    elif language == 'spanish':
        do = 'Do'
        re = 'Re'
        mi = 'Mi'
        fa = 'Fa'
        sol = 'Sol'
        la = 'La'
        si = 'Si'
    else:
        raise NotImplementedError('This language is not implemented.')

    # Unicode switch
    if unicode:
        sharp = '♯'
        flat = '♭'
    else:
        sharp = '#'
        flat = 'b'

    # Pitch class switch
    if pitch_class == 0:
        return do
    elif pitch_class == 1:
        if system == 'mixed':
            return do + sharp
        elif system == 'sharp':
            return do + sharp
        elif system == 'flat':
            return re + flat
        else:
            raise NotImplementedError('This system is not implemented.')
    elif pitch_class == 2:
        return re
    elif pitch_class == 3:
        if system == 'mixed':
            return mi + flat
        elif system == 'sharp':
            return re + sharp
        elif system == 'flat':
            return mi + flat
        else:
            raise NotImplementedError('This system is not implemented.')
    elif pitch_class == 4:
        return mi
    elif pitch_class == 5:
        return fa
    elif pitch_class == 6:
        if system == 'mixed':
            return fa + sharp
        elif system == 'sharp':
            return fa + sharp
        elif system == 'flat':
            return sol + flat
        else:
            raise NotImplementedError('This system is not implemented.')
    elif pitch_class == 7:
        return sol
    elif pitch_class == 8:
        if system == 'mixed':
            return la + flat
        elif system == 'sharp':
            return sol + sharp
        elif system == 'flat':
            return la + flat
        else:
            raise NotImplementedError('This system is not implemented.')
    elif pitch_class == 9:
        return la
    elif pitch_class == 10:
        if system == 'mixed':
            return si + flat
        elif system == 'sharp':
            return la + sharp
        elif system == 'flat':
            return si + flat
        else:
            raise NotImplementedError('This system is not implemented.')
    elif pitch_class == 11:
        return si
    else:
        raise ValueError('Parameter pitch_class should be comprised between 0 and 11.')
