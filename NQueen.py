from GeneticAlgo import GeneticAlgo
import random
import functools


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
        diagonal = lambda x1, y1, x2, y2: abs(x1 - x2) == abs(y1 - y2)

        return sum(
            diagonal(i, individual[i], j, individual[j])
            for i in range(len(individual))
            for j in range(i + 1, len(individual))
        )

    def crossover(self, parent1: list[int], parent2: list[int]) -> list[int]:
        # Order Crossover (OX) optimizado
        k = random.randint(1, self.n - 2)
        child = parent1[:k] + [None] * (self.n - k)
        used = set(parent1[:k])
        
        # Llenar posiciones restantes con elementos únicos de parent2 + faltantes
        remaining = [x for x in parent2 if x not in used] + [i for i in range(self.n) if i not in used]
        child[k:] = remaining[:self.n - k]
        
        return child

    def mutate(self, individual: list[int]) -> list[int]:
        # Swap mutation: intercambiar dos posiciones aleatorias
        individual = individual.copy()
        i = random.randint(0, self.n - 1)
        j = random.randint(0, self.n - 1)
        individual[i], individual[j] = individual[j], individual[i]
        return individual

    def local_search(self, individual: list[int]) -> list[int]:
        """Búsqueda local para mejorar un individuo específico."""
        current = individual.copy()
        current_fitness = self.fitness(current)
        
        # Si ya es óptimo, no hacer nada
        if current_fitness == 0:
            return current
        
        improved = True
        max_iterations = 50  # Limitar iteraciones para evitar bucles infinitos
        iterations = 0
        
        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            
            # Probar todos los swaps posibles
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    # Hacer swap
                    current[i], current[j] = current[j], current[i]
                    new_fitness = self.fitness(current)
                    
                    if new_fitness < current_fitness:
                        current_fitness = new_fitness
                        improved = True
                        # Si encontramos óptimo, salir inmediatamente
                        if new_fitness == 0:
                            return current
                        break
                    else:
                        # Deshacer swap si no mejora
                        current[i], current[j] = current[j], current[i]
                
                if improved:
                    break
        
        return current

    def end_condition(self, population: list[list[int]]) -> bool:
        has_solution = any(self.fitness(ind) == 0 for ind in population)
        max_generations_reached = self.gen >= self.iterations
        
        if has_solution:
            print(f"¡Solución encontrada en generación {self.gen}!")
        elif max_generations_reached:
            print(f"Máximo de generaciones alcanzado: {self.gen}")
            
        return has_solution or max_generations_reached
