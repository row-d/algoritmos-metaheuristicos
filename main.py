import typer
from rich.pretty import pprint
from rich.console import Console
from rich.table import Table
from typing import Annotated
from NQueen import NQueen
import os

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


def print_chessboard(solution: list[int], generation: int = None):
    """Imprime el tablero de ajedrez con las reinas usando Rich."""
    console = Console()
    n = len(solution)
    
    # Crear tabla sin encabezados
    table = Table(show_header=False, show_lines=True, title=f"Tablero {n}x{n} - N-Reinas")
    
    # Añadir columnas
    for _ in range(n):
        table.add_column(width=3, justify="center")
    
    # Crear filas del tablero
    for row in range(n):
        cells = []
        for col in range(n):
            if solution[col] == row:
                # Reina en esta posición
                cells.append("[bold red]♛[/bold red]")
            else:
                # Casilla vacía con patrón de tablero
                if (row + col) % 2 == 0:
                    cells.append("[on white] [/on white]")
                else:
                    cells.append("[on black] [/on black]")
        table.add_row(*cells)
    
    console.print(table)
    if generation is not None:
        console.print(f"\n[green]✓ Solución encontrada en la generación {generation}[/green]")


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
    sorted_population, population = nqueen.start(os.getenv("ELITISMO", False))
    
    # Extraer la mejor solución
    fitness_value, best_solution = sorted_population[0]
    
    print(f"\nGeneración: {nqueen.gen}")
    print("Mejor solución encontrada:")
    pprint(sorted_population[0])
    
    print(f"\nFitness de la mejor solución: {fitness_value}")
    if fitness_value == 0:
        print("¡Solución óptima encontrada! (0 conflictos)")
    else:
        print(f"Solución con {fitness_value} conflictos")
    
    print("\nTablero de ajedrez:")
    print_chessboard(best_solution, nqueen.gen)


if __name__ == "__main__":
    typer.run(n_queen)
