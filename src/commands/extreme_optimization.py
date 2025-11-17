import typer
from pathlib import Path
import numpy as np
from typing import Annotated
from src.utils.knapack_parser import knapack_parser
from src.core.algorithms.ExtremeOptimization import ExtremeOptimization


app = typer.Typer()


@app.command(name="extreme_optimization")
def extreme_optimization(
    filepath: Annotated[
        Path,
        typer.Argument(
            help="Ruta al archivo con las instancias del problema de la mochila.",
            resolve_path=True,
            exists=True,
            file_okay=True,
            dir_okay=False)
    ],
    iterations: Annotated[
        int,
        typer.Argument(
            help="Número máximo de iteraciones a ejecutar.")
    ],
    seed: Annotated[
        int,
        typer.Argument(
            help="Semilla para la generación de números aleatorios.")
    ],
    tau: Annotated[
        float,
        typer.Argument(
            help="Parámetro tau para la selección de componentes.")
    ],
):
    """Solucionador del problema de la mochila usando optimización extrema.
    """

    instances = knapack_parser(filepath)

    for instance in instances:
        optimizer = ExtremeOptimization(
            seed=seed,
            n_items=instance["n"],
            capacidad=instance["c"],
            tau=tau,
            precios=np.array(instance["precios"], dtype=np.int32),
            pesos=np.array(instance["pesos"], dtype=np.int32),
            max_iterations=iterations
        )

        _, precio_mejor_sol = optimizer.start()

        print(f"Instancia: {instance['title']}")
        print(f"Precio mejor solucion encontrada: {precio_mejor_sol}")
        print(f"Precio solucion optima: {instance['z']}")
        print(f"Diferencia: {precio_mejor_sol - instance['z']}")
        print("--------------------------------------------------")
