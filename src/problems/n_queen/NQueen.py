from src.core.algorithms.GeneticAlgo import GeneticAlgo
from src.core.EventEmitter import on
from src.utils.print_chessboard import print_chessboard
import random

class NQueen(GeneticAlgo[list[int]]):
    n: int
    iterations: int

    def __init__(
        self,
        seed: int,
        n: int,
        population_size: int,
        crossover_rate: float,
        mutation_rate: float,
        iterations: int,
    ):
        super().__init__(seed, population_size, mutation_rate, crossover_rate)
        self.n = n
        self.iterations = iterations

    def generate_population(self) -> list[list[int]]:
        return [
            random.sample(range(self.n), self.n) for _ in range(self.population_size)
        ]

    def fitness(self, individual: list[int]) -> float | int:
        def diagonal(x1, y1, x2, y2): return abs(x1 - x2) == abs(y1 - y2)

        return sum(
            diagonal(i, individual[i], j, individual[j])
            for i in range(len(individual))
            for j in range(i + 1, len(individual))
        )

    def crossover(self, parent1: list[int], parent2: list[int]) -> list[int]:
        k = random.randint(1, self.n - 2)
        child = parent1[:k] + [None] * (self.n - k)
        used = set(parent1[:k])
        remaining = [x for x in parent2 if x not in used] + [
            i for i in range(self.n) if i not in used
        ]
        child[k:] = remaining[: self.n - k]

        return child

    def __swap(self, individual: list[int], i: int, j: int) -> None:
        individual[i], individual[j] = individual[j], individual[i]

    def mutate(self, individual: list[int]) -> list[int]:
        individual = individual.copy()
        i = random.randint(0, self.n - 1)
        j = random.randint(0, self.n - 1)
        self.__swap(individual, i, j)
        return individual

    # @on('new_individual')
    def new_individual(
        self, generation: int, individual: list[int], fitness: float | int
    ):
        print(
            f"Generation {generation}: Individual {individual} with fitness {fitness}")
        if fitness <= 2:
            improved = self.local_search(individual)
            improved_fitness = self.fitness(improved)
            if improved_fitness < fitness:
                individual[:] = improved

    def local_search(self, individual: list[int]) -> list[int]:
        """Se hace mutacion forzada hasta llegar a un minimo local o encontrar la solucion"""
        current = individual.copy()
        current_fitness = self.fitness(current)

        if current_fitness == 0:
            return current

        improved = True

        while improved:
            improved = False

            for i in range(self.n):
                for j in range(i + 1, self.n):
                    self.__swap(current, i, j)
                    new_fitness = self.fitness(current)
                    if new_fitness < current_fitness:
                        current_fitness = new_fitness
                        improved = True
                        if new_fitness == 0:
                            return current
                        break
                    else:
                        self.__swap(current, i, j)
                if improved:
                    break
        return current

    def end_condition(self) -> bool:
        has_solution = any(fit == 0 for fit in
                           self.pop_fitness)
        max_generations_reached = self.gen >= self.iterations
        return has_solution or max_generations_reached

    @on('end')
    def on_end(self):
        """Imprime el mejor resultado al final del algoritmo"""
        best_fitness = min(self.pop_fitness)
        best_index = self.pop_fitness.index(best_fitness)
        best_individual = self.population[best_index]
        
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Mejor solución encontrada: {best_individual}")
        print(f"Fitness: {best_fitness}")
        print(f"Generaciones ejecutadas: {self.gen}")
        
        if best_fitness == 0:
            print("¡SOLUCIÓN PERFECTA ENCONTRADA!")
        
        print("\nTablero:")
        print_chessboard(best_individual)
