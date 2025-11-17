from pathlib import Path
from typing import TypedDict, Any


class KnapdackData(TypedDict):
    title: str
    n: int
    c: int
    z: int
    time: float
    precios: list[int]
    pesos: list[int]
    solucion_optima: list[int]


def default_knapack_data() -> KnapdackData:
    return {
        "title": "",
        "n": 0,
        "c": 0,
        "z": 0,
        "time": 0.0,
        "precios": [],
        "pesos": [],
        "solucion_optima": []
    }


def knapack_parser(path: Path) -> list[KnapdackData]:
    meta_values: list[KnapdackData] = []
    meta: KnapdackData = default_knapack_data()

    with open(path, "r") as file:
        while (line := file.readline()):
            data = line.strip().split(" ")
            tag = data[0]
            value = data[1] if len(data) > 1 else ""

            if tag.startswith("knap"):
                meta["title"] = tag
            if tag == "n":
                meta["n"] = int(value)
            if tag == "c":
                meta["c"] = int(value)
            if tag == "z":
                meta["z"] = int(value)
            if tag == "time":
                meta["time"] = float(value)
                pesos: list[int] = []
                precios: list[int] = []
                solucion_optima: list[int] = []

                for _ in range(meta["n"]):
                    line = file.readline()
                    item_data = [int(x) for x in line.strip().split(",")]
                    precios.append(item_data[1])
                    pesos.append(item_data[2])
                    solucion_optima.append(item_data[3])

                meta["pesos"] = pesos
                meta["precios"] = precios
                meta["solucion_optima"] = solucion_optima
            if tag == "-----":
                meta_values.append(meta.copy())
                meta = default_knapack_data()
    return meta_values
