import typer
from src.commands.acs import app as acsapp
from src.commands.n_queen import app as nqueenapp 

if __name__ == "__main__":
    app = typer.Typer()
    app.add_typer(acsapp)
    app.add_typer(nqueenapp)
    app()
