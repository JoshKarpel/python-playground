import asyncio
from pathlib import Path

import typer
from counterweight.app import app

from python_playground.conway import conway_ui
from python_playground.koch_snowflake import draw_kochs

cli = typer.Typer()


@cli.command()
def koch(output: Path = Path.cwd() / "outputs" / "koch") -> None:
    """Run the Koch snowflake generation."""
    draw_kochs(output)


@cli.command()
def conway() -> None:
    asyncio.run(app(conway_ui))


if __name__ == "__main__":
    cli()
