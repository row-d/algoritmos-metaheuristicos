import os
import typer
from rich.pretty import pprint
from typing import Annotated
from src.problems.n_queen.NQueen import NQueen
from src.utils.print_chessboard import print_chessboard

app = typer.Typer(
    help="Solucionador del problema de las N-Reinas usando algoritmos genéticos.",
    epilog="""
        Ejemplo de uso:
            python main.py 42 8 100 0.8 0.1 1000

        Esto ejecutará el algoritmo con:
        - Semilla: 42
        - Tablero: 8x8 (8 reinas)
        - Población: 100 individuos
        - Tasa de cruzamiento: 80%
        - Tasa de mutación: 10%
        - Máximo 1000 generaciones
    """,
)


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
            callback=lambda x: (
                x if x > 3 else typer.Exit("El número de reinas debe ser mayor a 3.")
            ),
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
            callback=lambda x: (
                x
                if 0 <= x <= 1
                else typer.Exit("La tasa de cruzamiento debe estar entre 0 y 1.")
            ),
        ),
    ],
    mutation_rate: Annotated[
        float,
        typer.Argument(
            help="Probabilidad de mutación de un individuo [0-1].",
            callback=lambda x: (
                x
                if 0 <= x <= 1
                else typer.Exit("La tasa de mutación debe estar entre 0 y 1.")
            ),
        ),
    ],
    iterations: Annotated[
        int,
        typer.Argument(
            help="Número máximo de generaciones a ejecutar.",
            callback=lambda x: (
                x
                if x > 0
                else typer.Exit("El número de iteraciones debe ser mayor a 0.")
            ),
        ),
    ],
):
    """Resuelve el problema de las N-Reinas usando algoritmos genéticos."""
    nqueen = NQueen(seed, n, population_size, crossover_rate, mutation_rate, iterations)
    nqueen.start(os.getenv("ELITISMO", False))

    
    

if __name__ == "__main__":
    typer.run(n_queen)
