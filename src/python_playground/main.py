import asyncio
from pathlib import Path

import typer
from counterweight.app import app

from python_playground.conway import conway_ui
from python_playground.koch_snowflake import draw_kochs
from python_playground.sound import make_sound

cli = typer.Typer(
    no_args_is_help=True,
)


@cli.command()
def koch(output: Path = Path.cwd() / "outputs" / "koch") -> None:
    """Run the Koch snowflake generation."""
    draw_kochs(output)


@cli.command()
def conway() -> None:
    """Run the Conway's Game of Life UI."""
    asyncio.run(app(conway_ui))


@cli.command()
def sound(output: Path = Path.cwd() / "outputs" / "sounds" / "sound.wav") -> None:
    """Run the sound generation."""
    make_sound(path=output)


if __name__ == "__main__":
    cli()
