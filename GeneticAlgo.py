from abc import ABC, abstractmethod
import random
import queue
import os


class GeneticAlgo[T](ABC):
    """Base class for a genetic algorithm.

    Attributes:
        gen (int): Current generation number.
        seed (float): Seed for random number generation.
        population_size (int): Size of the population.
        mutation_rate (float): Probability of mutation for an individual.
        crossover_rate (float): Probability of crossover between two parents.

    Methods:
        generate_population: Generates the initial population.
        fitness: Evaluates the fitness of an individual.
        crossover: Combines two parents to create a child.
        mutate: Mutates an individual.
        end_condition: Checks if the end condition for the algorithm is met.
        start: Runs the genetic algorithm until the end condition is met.

    """

    gen: int
    seed: float
    population_size: int
    mutation_rate: float
    crossover_rate: float

    def __init__(
        self,
        seed: float,
        population_size: int,
        mutation_rate: float,
        crossover_rate: float,
    ):
        self.seed = seed
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        random.seed(seed)

    @abstractmethod
    def generate_population(self) -> list[T]: ...

    @abstractmethod
    def fitness(self, individual: T) -> float | int: ...

    @abstractmethod
    def crossover(self, parent1: T, parent2: T) -> T: ...

    @abstractmethod
    def mutate(self, individual: T) -> T: ...

    @abstractmethod
    def end_condition(self, population: list[T]) -> bool: ...

    def __elitism_start(self):
        self.gen = 0
        population: list[T] = self.generate_population()
        fitness = [self.fitness(ind) for ind in population]
        sorted_population = sorted(zip(fitness, population), key=lambda x: x[0])
        
        while not self.end_condition(population):
            first, second = sorted_population[:2]
            temp_population = queue.PriorityQueue(self.population_size)
            temp_population.put(first)
            temp_population.put(second)

            while temp_population.qsize() < self.population_size:
                # Obtener padres y extraer solo los individuos
                parent1_tuple = temp_population.get()
                parent2_tuple = temp_population.get()
                parent1, parent2 = parent1_tuple[1], parent2_tuple[1]

                cross_chance = random.random()
                if cross_chance < self.crossover_rate:
                    child = self.crossover(parent1, parent2)
                    mut_chance = random.random()
                    if mut_chance < self.mutation_rate:
                        child = self.mutate(child)
                    child_fitness = self.fitness(child)
                    
                    # Aplicar búsqueda local si el fitness es 1 o 2 (casi óptimo)
                    if hasattr(self, 'local_search') and child_fitness <= 2:
                        improved_child = self.local_search(child)
                        improved_fitness = self.fitness(improved_child)
                        if improved_fitness < child_fitness:
                            child = improved_child
                            child_fitness = improved_fitness
                    
                    temp_population.put((child_fitness, child))
                else:
                    # Solo devolver uno de los padres
                    temp_population.put(parent1_tuple)
                
                # Siempre devolver los padres que usamos
                temp_population.put(parent1_tuple)
                temp_population.put(parent2_tuple)

            self.gen += 1
            print(f"Generación: {self.gen}")
            population = [item[1] for item in temp_population.queue]
            fitness = [self.fitness(ind) for ind in population]
            sorted_population = sorted(zip(fitness, population), key=lambda x: x[0])

        return sorted_population, population

    def start(self, elitism: bool = False):
        if elitism:
            return self.__elitism_start()
        self.gen = 0
        population: list[T] = self.generate_population()
        fitness = [self.fitness(ind) for ind in population]
        sorted_population = sorted(zip(fitness, population), key=lambda x: x[0])

        while not self.end_condition(population):
            temp_population = [x[1] for x in random.sample(sorted_population[:2], k=2)]

            while len(temp_population) < self.population_size:
                parents = random.sample(temp_population, k=2)
                parent1, parent2 = parents[0], parents[1]

                cross_chance = random.random()
                if cross_chance < self.crossover_rate:
                    child = self.crossover(parent1, parent2)
                    mut_chance = random.random()
                    if mut_chance < self.mutation_rate:
                        child = self.mutate(child)
                    
                    # Aplicar búsqueda local ocasionalmente (10% de probabilidad)
                    if hasattr(self, 'local_search') and random.random() < 0.1:
                        child = self.local_search(child)
                    
                    temp_population.append(child)
                else:
                    # Solo añadir un padre para evitar crecimiento desigual
                    temp_population.append(parent1)
                
                # Si nos pasamos del tamaño, truncar
                if len(temp_population) > self.population_size:
                    temp_population = temp_population[:self.population_size]

            self.gen += 1
            print(f"Generación: {self.gen}")
            population = temp_population
            fitness = [self.fitness(ind) for ind in population]
            sorted_population = sorted(zip(fitness, population), key=lambda x: x[0])

        return sorted_population, population
