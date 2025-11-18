from dataclasses import dataclass
import numpy as np
import numpy.typing as npt
from src.core.algorithms.selection.roulette import roulette


@dataclass
class ExtremeOptimization:
    seed: int
    n_items: int
    capacidad: int
    tau: float
    precios: npt.NDArray[np.int32]
    pesos: npt.NDArray[np.int32]
    max_iterations: int = 1
    iterations: int = 1
    optimal_solution: int | None = None

    def __post_init__(self):
        np.random.seed(self.seed)

    def start(self) -> tuple[npt.NDArray[np.int32], int]:
        solution: npt.NDArray[np.int32] = self.generar_solucion_inicial()
        fitness: npt.NDArray[np.float64] = self.precios / self.pesos
        best_sol: npt.NDArray[np.int32] = solution.copy()

        for i in range(1,self.max_iterations+1):
            alcanza_capacidad = np.sum(
                self.pesos[solution == 1]) <= self.capacidad

            if alcanza_capacidad:
                self.agregar_item(solution, fitness, 0)
            else:
                self.agregar_item(solution, fitness, 1)

            precio_sol = np.sum(solution * self.precios)
            precio_mejor_sol = np.sum(best_sol * self.precios)
            alcanza_capacidad = np.sum(
                self.pesos[solution == 1]) <= self.capacidad
            self.iterations = i
            if alcanza_capacidad and precio_sol > precio_mejor_sol:
                best_sol = solution.copy()
                if self.optimal_solution is not None and precio_sol == self.optimal_solution:
                    break

        return best_sol, np.sum(best_sol * self.precios, dtype=int)

    def generar_solucion_inicial(self) -> npt.NDArray[np.int32]:
        sol = np.zeros(self.n_items, dtype=np.int32)
        sol[np.random.randint(0, self.n_items)] = 1

        alcanza_capacidad = np.sum(
            self.pesos * sol) <= self.capacidad

        while not alcanza_capacidad:
            sol = np.zeros(self.n_items, dtype=np.int32)
            sol[np.random.randint(0, self.n_items)] = 1

        return sol

    def generar_vector_prob(self, n: int) -> npt.NDArray[np.float64]:
        vector_prob = np.arange(1, n + 1, dtype=float)
        vector_prob **= (-self.tau)
        return vector_prob

    def agregar_item(self, sol: npt.NDArray[np.int32], fitness: npt.NDArray[np.float64], valor: int) -> None:
        indices_sol = np.where(sol == valor)[0]
        sol_temporal = np.array(
            [indices_sol, fitness[indices_sol].astype(float)], dtype=object)

        sol_temporal = sol_temporal[:, np.argsort(
            sol_temporal[1])] if valor == 1 else sol_temporal[:, np.argsort(
                sol_temporal[1])[::-1]]

        vector_prob_temporal = self.generar_vector_prob(len(indices_sol))
        indice_temporal = roulette(vector_prob_temporal)

        sol[sol_temporal[0][indice_temporal]] = 1 if valor == 0 else 0
