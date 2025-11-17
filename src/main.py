import typer
from src.commands.acs import app as acsapp
from src.commands.n_queen import app as nqueenapp

from src.commands.extreme_optimization import app as eoapp

if __name__ == "__main__":
    app = typer.Typer()
    app.add_typer(acsapp)
    app.add_typer(nqueenapp)
    app.add_typer(eoapp)
    app()
