import typer
from algometa.commands.acs import app as acsapp
from algometa.commands.n_queen import app as nqueenapp

from algometa.commands.extreme_optimization import app as eoapp

app = typer.Typer()
app.add_typer(acsapp)
app.add_typer(nqueenapp)
app.add_typer(eoapp)

if __name__ == "__main__":
    app()
