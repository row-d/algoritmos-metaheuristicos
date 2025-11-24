from rich.console import Console
from rich.table import Table

def print_chessboard(solution: list[int], generation: int = None):
    """Imprime el tablero de ajedrez con las reinas usando Rich."""
    console = Console()
    n = len(solution)

    # Crear tabla sin encabezados
    table = Table(
        show_header=False, show_lines=True, title=f"Tablero {n}x{n} - N-Reinas"
    )

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
        console.print(
            f"\n[green]✓ Solución encontrada en la generación {generation}[/green]"
        )
