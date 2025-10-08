from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from counterweight.components import component
from counterweight.elements import Chunk, Div, Text
from counterweight.events import KeyPressed
from counterweight.hooks import use_state
from counterweight.keys import Key
from counterweight.styles.utilities import *
from PIL import Image
from structlog import get_logger

logger = get_logger()

cols = 80
scale = 0.43

chars = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-+~<>i!lI;:,\"^`'. "


@component
def grayscale_ui() -> Div:
    dir, set_dir = use_state(Path(os.getenv("GRAYSCALE_PATH", Path.cwd())))
    file_idx, set_file_idx = use_state(0)

    def on_key(event: KeyPressed) -> None:
        if event.key == Key.Right:
            set_file_idx(lambda idx: idx + 1)
        elif event.key == Key.Left:
            set_file_idx(lambda idx: idx - 1)

    file = sorted((p for p in dir.iterdir() if p.suffix == ".jpg"), key=lambda p: p.name)[file_idx]

    image = Image.open(file).convert("L")
    W, H = image.size[0], image.size[1]
    w = W / cols
    h = w / scale
    rows = int(H / h)

    logger.info("Image size", width=W, height=H, cols=cols, w=w, h=h)

    lines = []
    for r in range(rows):
        logger.info("Processing", row=r)
        y1 = int(r * h)
        y2 = int((r + 1) * h) if r == rows - 1 else H
        line = ""
        for c in range(cols):
            x1 = int(c * w)
            x2 = int((c + 1) * w) if c == cols - 1 else W
            img = image.crop((x1, y1, x2, y2))
            avg = int(np.average(img))
            gsval = chars[int((avg * (len(chars) - 1)) / 255)]
            line += gsval

        lines.append(line + "\n")

    return Div(
        style=col | align_children_center | justify_children_space_evenly | gap_children_2 | pad_1,
        children=[
            Text(style=border_heavy, content=f"Directory: {dir}, File: {file} (left/right to navigate)"),
            # Text(
            #     content=lines[0],
            # ),
            Text(
                content=[Chunk(content=line) for line in lines],
            ),
        ],
        on_key=on_key,
    )
