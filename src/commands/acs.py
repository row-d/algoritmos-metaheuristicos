from pathlib import Path
import typer
from typing import Annotated
from src.core.algorithms.AntColonySystem import AntColonySystem
import numpy as np

app = typer.Typer()

@app.command(name="acs")
def ant_colony_system(
    filename: Annotated[
        Path,
        typer.Argument(
            help="Ruta al archivo con las coordenadas de las ciudades.",
            resolve_path=True,
            exists=True,
            file_okay=True,
            dir_okay=False)
    ],
    seed: Annotated[
        int,
        typer.Argument(
            help="Semilla para la generación de números aleatorios.")
    ],
    ant_colony_size: Annotated[
        int,
        typer.Argument(
            help="Número de hormigas en la colonia.")
    ],
    iterations: Annotated[
        int,
        typer.Argument(
            help="Número máximo de iteraciones a ejecutar.")
    ],
    alpha: Annotated[
        float,
        typer.Argument(
            help="Importancia de la feromona en la elección del camino.")
    ],
    beta: Annotated[
        float,
        typer.Argument(
            help="Importancia de la visibilidad en la elección del camino.")],
    q0: Annotated[
        float,
        typer.Argument(
            help="Probabilidad de elegir el mejor camino (explotación).")
    ],
):
    """Solucionador del problema del agente viajero usando el sistema de colonia de hormigas.
    """

    with open(filename, 'r') as file:
        def get_meta(
            line: str) -> list[str]: return line.strip().split(": ")[1]

        _name, _type, _comment, _dimension, _edge_weight_type = [
            get_meta(file.readline()) for _ in range(5)]

        file.readline()  # Skip the "NODE_COORD_SECTION" line

        path = np.array([np.array([float(x), float(y)]) for _, x, y in (file.readline().strip().split(" ")
                                                                        for _ in range(int(_dimension)))])

    acs = AntColonySystem(seed, ant_colony_size, alpha,
                          beta, q0, iterations, path)
    acs.start()
