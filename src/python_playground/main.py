import asyncio
from pathlib import Path

import typer
from counterweight.app import app

from python_playground.conway import conway_ui
from python_playground.koch_snowflake import draw_kochs

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


if __name__ == "__main__":
    cli()
