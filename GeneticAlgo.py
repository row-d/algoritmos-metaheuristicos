from abc import ABC, abstractmethod
import random
import queue

class GeneticAlgo[T](ABC):
    """Base class for a genetic algorithm.
    
    Attributes:
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
    seed: float
    population_size: int
    mutation_rate: float
    crossover_rate: float
    
    def __init__(self, seed: float, population_size: int, mutation_rate: float, crossover_rate: float):
        self.seed = seed
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        random.seed(seed)

    @abstractmethod
    def generate_population(self) -> list[T]:

        ...
        
    @abstractmethod
    def fitness(self, individual: T) -> float:
        ...
        
    @abstractmethod
    def crossover(self, parent1: T, parent2: T) -> T:
        ...
        
    @abstractmethod
    def mutate(self, individual: T) -> T:
        ...
        
    @abstractmethod
    def end_condition(self, population: list[T]) -> bool:
        ...
        
    def start(self):
        gen = 0
        population = self.generate_population()
        fitness = [-self.fitness(ind) for ind in population]
        sorted_population = sorted(zip(fitness, population), key=lambda x: x[0])
        
        while not self.end_condition(population):
            first, second = sorted_population[:2]
            temp_population = queue.PriorityQueue(self.population_size)
            temp_population.put(first)
            temp_population.put(second)
            
            while temp_population.qsize() != self.population_size:
                parent1 = temp_population.get()
                parent2 = temp_population.get()
                cross_chance = random.random()
                if cross_chance < self.crossover_rate:
                    child = self.crossover(parent1[1], parent2[1])
                    mut_chance = random.random()
                    if mut_chance < self.mutation_rate:
                        child = self.mutate(child)
                    child_fitness = -self.fitness(child)
                    temp_population.put((child_fitness, child))
                else:
                    temp_population.put(parent1)
                    temp_population.put(parent2)
                    
            gen += 1
            population = [item[1] for item in temp_population.queue]
            fitness = [-self.fitness(ind) for ind in population]
            sorted_population = sorted(zip(fitness, population), key=lambda x: x[0])
            
        return sorted_population, population, gen
