from typing import Callable
import random
import queue


class GeneticAlgo[T]:
    seed: int
    population_size: int
    mutation_rate: float
    crossover_rate: float
    population_fn: Callable[[], list[T]] = None
    fitness_fn: Callable[[T], float] = None
    cross_fn: Callable[[T, T], T] = None
    mutate_fn: Callable[[T], T] = None
    end_condition: Callable[[T], bool] = None

    def start(self):
        gen = 0
        population = self.population_fn()
        fitness = [-self.fitness_fn(ind) for ind in population]
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
                    child = self.cross_fn(parent1[1], parent2[1])
                    mut_chance = random.random()
                    if mut_chance < self.mutation_rate:
                        child = self.mutate_fn(child)
                    child_fitness = -self.fitness_fn(child)
                    temp_population.put((child_fitness, child))
                else:
                    temp_population.put(parent1)
                    temp_population.put(parent2)
            gen += 1
            population = temp_population.get_all()
            fitness = [-self.fitness_fn(ind) for ind in population]
            sorted_population = sorted(zip(fitness, population), key=lambda x: x[0])
        return sorted_population, population, gen
