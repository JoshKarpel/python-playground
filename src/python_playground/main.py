from pathlib import Path

import typer

from python_playground.conway import Conway
from python_playground.koch_snowflake import draw_kochs

app = typer.Typer()


@app.command()
def koch(output: Path = Path.cwd() / "outputs" / "koch") -> None:
    """Run the Koch snowflake generation."""
    draw_kochs(output)


@app.command()
def conway() -> None:
    conway = Conway.zeros(width=10, height=10)

    conway.upsert_glider(1, 1)
    conway.print()

    for _ in range(4):
        conway.step()
        conway.print()


if __name__ == "__main__":
    app()
