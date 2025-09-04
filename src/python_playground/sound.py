from __future__ import annotations

import math
import wave
from collections import deque
from datetime import timedelta
from math import pi
from pathlib import Path

import numpy as np

tau = 2 * pi
DECAY = 0.995


def karplus_strong(frequency: float, duration: timedelta, sample_rate: float) -> np.ndarray:
    num_samples = math.ceil(sample_rate * duration.total_seconds())
    buffer_len = math.ceil(sample_rate / frequency)
    print(num_samples, buffer_len)
    buffer = deque(np.random.uniform(low=-0.5, high=0.5, size=num_samples).tolist(), maxlen=buffer_len)
    samples = np.zeros(num_samples, dtype=np.float32)

    for idx in range(num_samples):
        first, second = buffer[0], buffer[1]
        new_last = DECAY * 0.5 * (first + second)

        samples[idx] = first

        # Because the buffer has a max length,
        # appending automatically pops the first element.
        buffer.append(new_last)

    return samples


DTYPE = np.int16
MAX_INT16 = np.iinfo(DTYPE).max


def to_int16(samples: np.ndarray) -> np.ndarray:
    return (samples * MAX_INT16).astype(DTYPE)


def write_wav_from_samples(path: Path, samples: np.ndarray, sample_rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)  # mono
        f.setsampwidth(2)  # 2 bytes for int16
        f.setframerate(sample_rate)
        f.setnframes(len(samples))
        f.writeframes(to_int16(samples).tobytes())


def make_sound(path: Path) -> None:
    sample_rate = 44100  # Hz
    duration = timedelta(seconds=3)
    frequency = 220  # Hz

    samples = karplus_strong(frequency, duration, sample_rate)

    write_wav_from_samples(path, samples, sample_rate)
