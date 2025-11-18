import typer
from pathlib import Path
import numpy as np
from typing import Annotated, Optional
from src.utils.knapack_parser import knapack_parser
from src.core.algorithms.ExtremeOptimization import ExtremeOptimization

app = typer.Typer()


@app.command(name="eo")
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
    folder_output: Annotated[
        Optional[Path],
        typer.Option(
            "--output",
            "-o",
            help="Ruta de la carpeta de salida.",
            resolve_path=True,
            file_okay=False,
            dir_okay=True)
    ] = None,
    silent: Annotated[
        Optional[bool],
        typer.Option(
            "--silent",
            "-s",
            help="Si se activa, no se imprimen los resultados en consola.",
            is_flag=True
        )
    ] = False
):
    """Solucionador del problema de la mochila usando optimización extrema.
    """

    instances = knapack_parser(filepath)
    filename = f"result_eo_n{instances[0]['n']}_c{instances[0]['c']}_tau{tau}_seed{seed}.csv"
    output_file = open(folder_output / filename,
                       "w") if folder_output is not None else None
    if output_file:
        output_file.write(
            "Instancia,Iteraciones,Items,Capacidad,Precio Mejor Solucion,Precio Solucion Optima,Diferencia\n")

    for instance in instances:
        optimizer = ExtremeOptimization(
            seed=seed,
            n_items=instance["n"],
            capacidad=instance["c"],
            tau=tau,
            precios=np.array(instance["precios"], dtype=np.int32),
            pesos=np.array(instance["pesos"], dtype=np.int32),
            max_iterations=iterations,
            optimal_solution=instance["z"]
        )

        _, precio_mejor_sol = optimizer.start()
        if not silent:
            print(f"Instancia: {instance['title']}")
            print(f"Precio mejor solucion encontrada: {precio_mejor_sol}")
            print(f"Precio solucion optima: {instance['z']}")
            print(f"Diferencia: {precio_mejor_sol - instance['z']}")
            print("--------------------------------------------------")
        if output_file:
            output_file.write(
                f"{instance['title']},{optimizer.iterations},{instance['n']},{instance['c']},{precio_mejor_sol},{instance['z']},{precio_mejor_sol - instance['z']}\n")

    if output_file:
        output_file.close()
