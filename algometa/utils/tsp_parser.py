"""Utilidades para parsear archivos TSP (Travelling Salesman Problem)."""

import numpy as np
from pathlib import Path


def parse_tsp_file(filename: Path) -> np.ndarray:
    """
    Lee un archivo TSP y extrae las coordenadas de las ciudades.

    Args:
        filename: Ruta al archivo TSP que contiene las coordenadas de las ciudades.

    Returns:
        np.ndarray: Array de coordenadas (x, y) de las ciudades.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el formato del archivo no es válido.
    """
    coordinates = []
    meta_data = {}

    def get_meta(line: str) -> str:
        """Extrae el valor de una línea de metadatos del formato 'CLAVE: valor'."""
        data = line.strip().split(": ")
        return (data[0], data[1]) if len(data) == 2 else (line.strip(), None)

    with open(filename, 'r') as file:
        while (line := file.readline()):
            tag, value = get_meta(line)
            
            if value:
                meta_data[tag] = value
                
            if tag == "NODE_COORD_SECTION":
                dimension = meta_data.get("DIMENSION", None)
                for _ in range(int(dimension)):
                    line = file.readline().strip()
                    if not line:
                        break
                    parts = line.split()
                    if len(parts) >= 3:
                        # Formato: índice x y
                        _, x, y = parts[0], parts[1], parts[2]
                        coordinates.append([float(x), float(y)])
        return np.array([np.array(coord) for coord in coordinates])
