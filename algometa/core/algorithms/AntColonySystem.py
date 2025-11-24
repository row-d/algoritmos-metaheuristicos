from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np
import numpy.typing as npt
import math


@dataclass
class AntColonySystem(ABC):
    seed: int
    colony_size: int
    alpha: float
    beta: float
    q0: float
    max_iterations: int
    nodes: npt.NDArray
    it: int = 0
    
    def __post_init__(self):
        np.random.seed(self.seed)

    def end_condition(self):
        return self.it == self.max_iterations

    def roulette(self, values: npt.NDArray) -> int:
        total = np.sum(values)
        pick = np.random.uniform(0, total)
        current = 0
        for i, value in enumerate(values):
            current += value
            if current > pick:
                return i
        return 0

    def next_node(self, i: int, visited_mask: npt.NDArray) -> int:
        q = np.random.rand()
        not_visited = ~visited_mask

        # Obtener índices de nodos no visitados
        available_nodes = np.where(not_visited)[0]

        if len(available_nodes) == 0:
            return 0  # No hay nodos disponibles

        # Calcular valores τ * η^β solo para nodos no visitados
        tau_eta_values = np.array([
            (self.pheromones[i, j]) * (self.heuristics[i, j] ** self.beta)
            for j in available_nodes
        ])

        if q <= self.q0:
            # Explotación: elegir el mejor nodo disponible
            best_idx = np.argmax(tau_eta_values)
            return available_nodes[best_idx]
        else:
            # Exploración: usar ruleta entre nodos no visitados
            if np.sum(tau_eta_values) == 0:
                # Si todos los valores son 0, elegir aleatoriamente
                return np.random.choice(available_nodes)
            return available_nodes[self.roulette(tau_eta_values)]

    def cost(self, solution: npt.NDArray) -> float:
        return sum(np.linalg.norm(
            self.nodes[solution[i]] - self.nodes[solution[i - 1]]) for i in range(len(solution)))

    def update_local_pheromone(self, i: int, j: int) -> float:
        return (1 - self.alpha) * self.pheromones[i, j] + self.alpha * self.Tij0

    def update_global_pheromone(self, best_solution: npt.NDArray) -> npt.NDArray:
        pheromones = (1 - self.alpha) * self.pheromones
        for i in range(len(self.nodes)):
            j = best_solution[i]
            k = best_solution[i - 1]
            pheromones[j, k] += self.alpha / self.cost(best_solution)
        return pheromones

    def get_best(self, colony: npt.NDArray):
        return colony[np.argmax([1/self.cost(sol) for sol in colony])]

    def start(self) -> npt.NDArray:
        n = len(self.nodes)
        self.best_solution = np.random.permutation(n)
        self.Tij0 = 1 / (n * self.cost(self.best_solution))
        self.pheromones = np.full((n, n), self.Tij0, dtype=np.float64)

        # Corregir cálculo de heurísticas
        self.heuristics = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    distance = np.linalg.norm(self.nodes[i] - self.nodes[j])
                    self.heuristics[i, j] = 1 / distance if distance > 0 else 0

        while not self.end_condition():
            visited = np.zeros((self.colony_size, n), dtype=bool)
            colony = np.full((self.colony_size, n), -1, dtype=int)

            # Inicializar hormigas con nodos aleatorios
            for ant in range(self.colony_size):
                start_node = np.random.randint(n)
                colony[ant, 0] = start_node
                visited[ant, start_node] = True

            # Construir soluciones para cada hormiga
            for step in range(1, n):
                for ant in range(self.colony_size):
                    current_node = colony[ant, step - 1]
                    j = self.next_node(current_node, visited[ant])
                    colony[ant, step] = j
                    visited[ant, j] = True
                    self.pheromones[current_node, j] = self.update_local_pheromone(
                        current_node, j)

            # Conectar último nodo con el primero para completar el ciclo
            for ant in range(self.colony_size):
                first_node = colony[ant, 0]
                last_node = colony[ant, -1]
                self.pheromones[last_node, first_node] = self.update_local_pheromone(
                    last_node, first_node)

            new_best = self.get_best(colony)
            if self.cost(new_best) < self.cost(self.best_solution):
                self.best_solution = new_best
            self.pheromones = self.update_global_pheromone(self.best_solution)
            self.it += 1
        return self.best_solution
