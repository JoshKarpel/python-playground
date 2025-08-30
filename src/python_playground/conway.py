from __future__ import annotations

from asyncio import sleep
from dataclasses import dataclass
from random import randint
from typing import Self

import numpy as np
import numpy.typing as npt
from counterweight.components import component
from counterweight.elements import Chunk, Div, Text
from counterweight.events import KeyPressed
from counterweight.hooks import use_effect, use_state
from counterweight.keys import Key
from counterweight.styles.utilities import *
from more_itertools import grouper
from structlog import get_logger

logger = get_logger()

dtype = np.uint8
Cells = npt.NDArray[dtype]

WHITE = Color.from_name("white")
BLACK = Color.from_name("black")

GLIDER = np.array(
    [
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
    ],
)

GLIDER_GUN_SQUARE = np.array(
    [
        [1, 1],
        [1, 1],
    ]
)
GLIDER_GUN_CIRCLE = np.array(
    [
        [0, 0, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0],
    ]
)
GLIDER_GUN_U = np.array(
    [
        [0, 0, 0, 0, 1],
        [0, 0, 1, 0, 1],
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 0, 1],
    ]
)


@dataclass(frozen=True, slots=True)
class Conway:
    cells: Cells

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Conway):
            return NotImplemented
        return np.array_equal(self.cells, other.cells)

    def __hash__(self) -> int:
        return hash(self.cells.tobytes())

    @property
    def width(self) -> int:
        return self.cells.shape[1]

    @property
    def height(self) -> int:
        return self.cells.shape[0]

    @classmethod
    def zeros(cls, width: int, height: int) -> Self:
        return cls(
            cells=np.zeros((height, width), dtype=dtype),
        )

    @classmethod
    def random(cls, width: int, height: int, density: float = 0.5) -> Self:
        return cls(
            cells=np.where(np.random.rand(height, width) <= density, 1, 0),
        )

    def insert_glider(self, x: int, y: int) -> Self:
        new_cells = self.cells.copy()
        new_cells[y : y + GLIDER.shape[0], x : x + GLIDER.shape[1]] = GLIDER

        return type(self)(cells=new_cells)

    def insert_gosper_glider_gun(self, x: int, y: int) -> Self:
        new_cells = self.cells.copy()

        left_square_y = y + 5
        new_cells[
            left_square_y : left_square_y + GLIDER_GUN_SQUARE.shape[0],
            x : x + GLIDER_GUN_SQUARE.shape[1],
        ] = GLIDER_GUN_SQUARE

        circle_y = y + 3
        circle_x = x + 10
        new_cells[
            circle_y : circle_y + GLIDER_GUN_CIRCLE.shape[0], circle_x : circle_x + GLIDER_GUN_CIRCLE.shape[1]
        ] = GLIDER_GUN_CIRCLE

        u_y = y + 1
        u_x = circle_x + 10
        new_cells[
            u_y : u_y + GLIDER_GUN_U.shape[0],
            u_x : u_x + GLIDER_GUN_U.shape[1],
        ] = GLIDER_GUN_U

        right_square_y = y + 3
        right_square_x = u_x + 14
        new_cells[
            right_square_y : right_square_y + GLIDER_GUN_SQUARE.shape[0],
            right_square_x : right_square_x + GLIDER_GUN_SQUARE.shape[1],
        ] = GLIDER_GUN_SQUARE

        return type(self)(cells=new_cells)

    def step(self) -> Self:
        neighbors = sum(
            np.roll(np.roll(self.cells, dy, axis=0), dx, axis=1)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (dx != 0 or dy != 0)
        )

        is_on_and_has_2_or_3_neighbors = (self.cells == 1) & ((neighbors == 2) | (neighbors == 3))
        is_off_and_has_3_neighbors = (self.cells == 0) & (neighbors == 3)

        new_cells = np.where(
            is_on_and_has_2_or_3_neighbors | is_off_and_has_3_neighbors,
            1,
            0,
        )

        return type(self)(cells=new_cells)

    def print(self) -> None:
        print(self.cells)

    def canvas(self) -> list[Chunk]:
        return canvas(
            width=self.width,
            height=self.height,
            cells={(x, y): WHITE for x in range(self.width) for y in range(self.height) if self.cells[y, x] == 1},
        )


def canvas(
    width: int,
    height: int,
    cells: dict[tuple[int, int], Color],
) -> list[Chunk]:
    c: list[Chunk] = []
    for y_top, y_bot in grouper(range(height), 2):
        c.extend(
            Chunk(
                content="▀",
                style=CellStyle(
                    foreground=cells.get((x, y_top), BLACK),
                    background=cells.get((x, y_bot), BLACK),
                ),
            )
            for x in range(width)
        )
        c.append(Chunk.newline())
    c.pop()  # strip off last newline
    return c


w, h = 60, 60


@component
def conway_ui() -> Div:
    interval, set_interval = use_state(0.3)
    paused, set_paused = use_state(False)
    conway, set_conway = use_state(lambda: Conway.random(width=w, height=h, density=0.3))

    def on_key(event: KeyPressed) -> None:
        match event.key:
            case Key.Space:
                set_paused(lambda p: not p)
            case Key.Down:
                set_interval(lambda n: max(0.1, n - 0.1))
            case Key.Up:
                set_interval(lambda n: n + 0.1)
            case "r":
                set_conway(Conway.random(width=w, height=h, density=0.3))
            case "g":
                set_conway(Conway.zeros(width=w, height=h).insert_glider(randint(0, w - 3), randint(0, h - 3)))
            case "G":
                set_conway(Conway.zeros(width=w, height=h).insert_gosper_glider_gun(1, h // 2))

    def step(conway: Conway) -> Conway:
        return conway.step()

    async def tick() -> None:
        if paused:
            return
        while True:
            await sleep(interval)
            set_conway(step)

    use_effect(
        tick,
        deps=(
            interval,
            paused,
        ),
    )

    return Div(
        on_key=on_key,
        style=col | align_children_center | justify_children_space_evenly | gap_children_2 | pad_1,
        children=[
            Div(
                children=[
                    Text(
                        style=text_justify_center,
                        content=[
                            Chunk(content="Conway's Game of Life"),
                            Chunk.newline(),
                            Chunk.newline(),
                            Chunk(content=f"Interval: {interval:.1f}s (Up/Down to change)"),
                            Chunk.newline(),
                            Chunk(content="Press 'r' for random, 'g' for glider"),
                            Chunk.newline(),
                            Chunk(content="Press Ctrl+C to exit"),
                        ],
                    )
                ]
            ),
            Text(
                style=border_heavy | border_slate_500,
                content=conway.canvas(),
            ),
        ],
    )
