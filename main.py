import typer
from typing import Annotated
from NQueen import NQueen

app = typer.Typer()


@app.command()
def n_queen(
    seed: Annotated[
        int,
        typer.Argument(
            help="Semilla para la generación de números aleatorios.",
        ),
    ],
    n: Annotated[
        int,
        typer.Argument(
            help="Número de reinas y tamaño del tablero (NxN).",
            callback=lambda x: x > 3 or typer.Exit("El número de reinas debe ser mayor a 3."),
        ),
    ],
    population_size: Annotated[
        int,
        typer.Argument(
            help="Tamaño de la población en cada generación. Valores típicos: 50-200."
        ),
    ],
    crossover_rate: Annotated[
        float,
        typer.Argument(
            help="Probabilidad de cruzamiento entre individuos [0-1].",
            callback=lambda x: 0 <= x <= 1 or typer.Exit("La tasa de cruzamiento debe estar entre 0 y 1."),
        ),
    ],
    mutation_rate: Annotated[
        float,
        typer.Argument(
            help="Probabilidad de mutación de un individuo [0-1].",
            callback=lambda x: 0 <= x <= 1 or typer.Exit("La tasa de mutación debe estar entre 0 y 1."),
        ),
    ],
    iterations: Annotated[
        int,
        typer.Argument(
            help="Número máximo de generaciones a ejecutar.",
            callback=lambda x: x > 0 or typer.Exit("El número de iteraciones debe ser mayor a 0.")
        ),
    ],
):
    """Resuelve el problema de las N-Reinas usando algoritmos genéticos."""
    nqueen = NQueen(seed, n, population_size, crossover_rate, mutation_rate, iterations)
    nqueen.start()


if __name__ == "__main__":
    app()
