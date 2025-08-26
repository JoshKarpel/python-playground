import typer
from python_playground.koch_snowflake import draw_kochs

from pathlib import Path

app = typer.Typer()


@app.command()
def koch(output: Path = Path.cwd() / "outputs" / "koch"):
    """Run the Koch snowflake generation."""
    draw_kochs(output)


@app.command(hidden=True)
def dummy(): ...


if __name__ == "__main__":
    app()
