from GeneticAlgo import GeneticAlgo


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
        raise NotImplementedError("This method should be implemented")

    def fitness(self, individual: list[int]) -> float:
        raise NotImplementedError("This method should be implemented")

    def crossover(self, parent1: list[int], parent2: list[int]) -> list[int]:
        raise NotImplementedError("This method should be implemented")

    def mutate(self, individual: list[int]) -> list[int]:
        raise NotImplementedError("This method should be implemented")

    def end_condition(self, population: list[list[int]]) -> bool:
        raise NotImplementedError("This method should be implemented")
