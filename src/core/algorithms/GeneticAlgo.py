from abc import ABC, abstractmethod
import random
import queue
from src.core.EventEmitter import EventEmitter
from typing import Callable, Any, Iterable


class GeneticAlgo[T](ABC, EventEmitter):
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
    population: list[T]
    pop_fitness: list[float | int]
    __event_emitter__: EventEmitter

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
        super().__init__()

    @abstractmethod
    def generate_population(self) -> list[T]: ...

    @abstractmethod
    def fitness(self, individual: T) -> float | int: ...

    @abstractmethod
    def crossover(self, parent1: T, parent2: T) -> T: ...

    @abstractmethod
    def mutate(self, individual: T) -> T: ...

    @abstractmethod
    def end_condition(self) -> bool: ...

    def roulette(self, iter_list: Iterable[Any], key: Callable[[Any], float] = None) -> int:
        """Implements roulette wheel selection.

        Args:
            iter_list: Iterable of items to select from
            key: Function to extract fitness value from each item (if None, use items directly)

        Returns:
            Index of the selected item
        """
        values = [key(item) if key else item for item in iter_list]
        total_fitness = sum(values)
        pick = random.uniform(0, total_fitness)
        current = 0
        i = len(values) - 1
        for index, fitness in enumerate(values):
            current += fitness
            if current > pick:
                i = index
                break
        return i

    def deterministic_tournament(self, iter_list: Iterable[Any], key: Callable[[Any], float] = None, k: int = 3) -> int:
        """Implements deterministic tournament selection.
        Args:
            iter_list: Iterable of items to select from
            key: Function to extract fitness value from each item (if None, use items directly)
            k: Number of individuals to sample for the tournament
        Returns:
            List of indices of the selected items
        """

        sampled = random.sample(list(enumerate(iter_list)), k)
        if key:
            sampled.sort(key=lambda x: key(x[1]))
        else:
            sampled.sort(key=lambda x: x[1])
        return sampled[0][0]

    def probabilistic_tournament(self, iter_list: Iterable[Any], key: Callable[[Any], float] = None, k: int = 3, p: float = 0.75) -> list[int]:
        """Implements probabilistic tournament selection.
        Args:
            iter_list: Iterable of items to select from
            key: Function to extract fitness value from each item (if None, use items directly)
            k: Number of individuals to sample for the tournament
            p: Probability of selecting the best individual in the tournament
        Returns:
            List of indices of the selected items
        """

        sampled = random.sample(list(enumerate(iter_list)), k)
        if key:
            sampled.sort(key=lambda x: key(x[1]))
        else:
            sampled.sort(key=lambda x: x[1])
        for _ in range(k):
            r = random.random()
            for i in range(k):
                if r < p * (1 - p) ** i:
                    return sampled[i][0]
        return sampled[-1][0]

    def __elitism_start(self, selection_method: str = "roulette", custom_selection_method: Callable[[list[int | float]], int] | None = None) -> list[tuple[float | int, T]]:
        methods = {
            "roulette": self.roulette,
            "deterministic_tournament": self.deterministic_tournament,
            "probabilistic_tournament": self.probabilistic_tournament,
            "custom": custom_selection_method
        }
        select = methods.get(selection_method, self.roulette)
        
        self.gen = 0
        self.population: list[T] = self.generate_population()
        self.emit("initial_population", self.gen, self.population)
        
        self.pop_fitness = [self.fitness(ind) for ind in self.population]
        sorted_population = sorted(zip(self.pop_fitness, self.population), key=lambda x: x[0])
        self.emit("evaluated_population", self.gen, sorted_population)

        while not self.end_condition():
            # Keep the best individual (elitism)
            best_fitness, best_individual = sorted_population[0]
            temp_population = [best_individual]
            fitness_temp = [best_fitness]
            
            # Generate the rest of the population
            while len(temp_population) < self.population_size:
                # SELECTION - select parents from current population
                parent1_idx = select(self.pop_fitness)
                parent2_idx = select(self.pop_fitness)
                parent1 = self.population[parent1_idx]
                parent2 = self.population[parent2_idx]

                cross_chance = random.random()
                if cross_chance < self.crossover_rate:
                    # CROSSOVER
                    child = self.crossover(parent1, parent2)
                    self.emit("crossover", self.gen, parent1, parent2, child)
                    
                    mut_chance = random.random()
                    if mut_chance < self.mutation_rate:
                        # MUTATION
                        child = self.mutate(child)
                        self.emit("mutated", self.gen, child, self.fitness(child))
                    
                    # EVALUATION
                    child_fitness = self.fitness(child)
                    self.emit("new_individual", self.gen, child, child_fitness)
                    
                    temp_population.append(child)
                    fitness_temp.append(child_fitness)
                else:
                    # If no crossover, add one of the parents
                    temp_population.append(parent1)
                    fitness_temp.append(self.fitness(parent1))

            self.gen += 1
            self.population = temp_population
            self.pop_fitness = fitness_temp
            sorted_population = sorted(zip(self.pop_fitness, self.population), key=lambda x: x[0])
            self.emit("new_generation", self.gen, sorted_population)

        self.emit("end")
        return sorted_population

    def start(self,
              elitism: bool = False,
              selection_method: str = "roulette",
              custom_selection_method: Callable[[list[int | float]], int] | None = None) -> list[tuple[float | int, T]]:
        """Runs the genetic algorithm until the end condition is met.

        Args:
            elitism (bool, optional): Select the best parents for crossover. Defaults to False.
            selection_method (str, optional): Selection method to use ('roulette', 'deterministic_tournament', 'probabilistic_tournament'). Defaults to 'roulette'.
            custom_selection_method: Custom selection function when selection_method is 'custom'.
        """

        if selection_method == "custom" and custom_selection_method is None:
            raise ValueError(
                "Custom selection method must be provided when selection_method is 'custom'")

        if elitism:
            return self.__elitism_start(selection_method, custom_selection_method)

        methods = {
            "roulette": self.roulette,
            "deterministic_tournament": self.deterministic_tournament,
            "probabilistic_tournament": self.probabilistic_tournament,
            "custom": custom_selection_method
        }
        select = methods.get(selection_method, self.roulette)

        self.gen = 0
        self.population: list[T] = self.generate_population()
        self.pop_fitness = [self.fitness(ind) for ind in self.population]

        while not self.end_condition():
            temp_population = []
            fitness_temp = []

            while len(temp_population) < self.population_size:
                # SELECTION
                parent1_idx = select(self.pop_fitness)
                parent2_idx = select(self.pop_fitness)
                parent1 = self.population[parent1_idx]
                parent2 = self.population[parent2_idx]

                cross_chance = random.random()
                if cross_chance < self.crossover_rate:
                    # CROSSOVER
                    child = self.crossover(parent1, parent2)
                    self.emit("crossover", self.gen, parent1, parent2, child)
                    
                    mut_chance = random.random()
                    if mut_chance < self.mutation_rate:
                        # MUTATION
                        child = self.mutate(child)
                        self.emit("mutated", self.gen, child, self.fitness(child))
                    
                    # EVALUATION
                    child_fitness = self.fitness(child)
                    self.emit("new_individual", self.gen, child, child_fitness)
                    
                    temp_population.append(child)
                    fitness_temp.append(child_fitness)
                else:
                    temp_population.append(parent1)
                    fitness_temp.append(self.fitness(parent1))
                    if len(temp_population) < self.population_size:
                        temp_population.append(parent2)
                        fitness_temp.append(self.fitness(parent2))

            self.gen += 1
            self.population = temp_population[:self.population_size]
            self.pop_fitness = fitness_temp[:self.population_size]
            self.emit("new_generation", self.gen, list(zip(self.pop_fitness, self.population)))

        self.emit("end")
        return sorted(zip(self.pop_fitness, self.population), key=lambda x: x[0])
