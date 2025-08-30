from __future__ import annotations

from dataclasses import dataclass
from typing import Self

import numpy as np
import numpy.typing as npt

dtype = np.uint8
Cells = npt.NDArray[dtype]


@dataclass(slots=True)
class Conway:
    width: int
    height: int
    cells: Cells

    @classmethod
    def zeros(cls, width: int, height: int) -> Self:
        return cls(
            width=width,
            height=height,
            cells=np.zeros((height, width), dtype=dtype),
        )

    @classmethod
    def random(cls, density: float, width: int, height: int) -> Self:
        return cls(
            width=width,
            height=height,
            cells=np.where(np.random.rand(height, width) <= density, 1, 0),
        )

    def upsert_glider(self, x: int, y: int) -> None:
        self.cells[y : y + 3, x : x + 3] = np.array(
            [
                [0, 0, 1],
                [1, 0, 1],
                [0, 1, 1],
            ],
            dtype=dtype,
        )

    def step(self) -> None:
        neighbors = sum(
            np.roll(np.roll(self.cells, dy, axis=0), dx, axis=1)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (dx != 0 or dy != 0)
        )
        is_on_and_has_2_or_3_neighbors = (self.cells == 1) & ((neighbors == 2) | (neighbors == 3))
        is_off_and_has_3_neighbors = (self.cells == 0) & (neighbors == 3)
        self.cells = np.where(
            is_on_and_has_2_or_3_neighbors | is_off_and_has_3_neighbors,
            1,
            0,
        )

    def print(self) -> None:
        print(self.cells)
