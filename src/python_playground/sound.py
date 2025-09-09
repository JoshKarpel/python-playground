from __future__ import annotations

import math
import wave
from collections import deque
from dataclasses import dataclass
from datetime import timedelta
from math import pi
from pathlib import Path
from random import choice, uniform

import numpy as np

tau = 2 * pi


def make_sound_zeros(duration: timedelta, sample_rate: float) -> np.ndarray:
    num_samples = math.ceil(sample_rate * duration.total_seconds())
    return np.zeros(num_samples, dtype=np.float32)


def offset_index(offset: timedelta, sample_rate: float) -> int:
    return math.ceil(offset.total_seconds() * sample_rate)


def karplus_strong(frequency: float, duration: timedelta, sample_rate: float, decay: float) -> np.ndarray:
    buffer_len = math.ceil(sample_rate / frequency)
    buffer = deque(np.random.uniform(low=-0.5, high=0.5, size=buffer_len).tolist(), maxlen=buffer_len)

    samples = make_sound_zeros(duration, sample_rate)
    for idx in range(len(samples)):
        first, second = buffer[0], buffer[1]
        new_last = decay * 0.5 * (first + second)

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


@dataclass(slots=True)
class Samples:
    samples: np.ndarray
    sample_rate: int
    duration: timedelta

    @classmethod
    def zeros(cls, duration: timedelta, sample_rate: int) -> Samples:
        return cls(
            samples=make_sound_zeros(duration=duration, sample_rate=sample_rate),
            sample_rate=sample_rate,
            duration=duration,
        )

    def add_karplus_strong(
        self, frequency: float, start: timedelta, amplitude: float = 1, decay: float = 0.995
    ) -> None:
        start_idx = offset_index(start, self.sample_rate)
        duration = self.duration - start

        # Some trickery to avoid off-by-one errors
        slice = self.samples[start_idx:]
        slice[:] += (
            amplitude
            * karplus_strong(frequency=frequency, duration=duration, sample_rate=self.sample_rate, decay=decay)[
                : len(slice)
            ]
        )

    def write_wav(self, path: Path) -> None:
        write_wav_from_samples(path, self.samples, self.sample_rate)


def make_sound(path: Path) -> None:
    sample_rate = 44100  # Hz

    d = 20
    duration = timedelta(seconds=d + 1)
    freqs = [440, 493.88, 523.25, 587.33, 659.25, 698.46, 783.99]  # A4 to G5

    samples = Samples.zeros(duration=duration, sample_rate=sample_rate)

    for n in range(d):
        samples.add_karplus_strong(
            frequency=choice(freqs), start=timedelta(seconds=n + uniform(-0.25, 0.25)), decay=0.998
        )
        samples.add_karplus_strong(
            frequency=choice(freqs), start=timedelta(seconds=n + uniform(-0.25, 0.25)), decay=0.998
        )

    samples.write_wav(path)
