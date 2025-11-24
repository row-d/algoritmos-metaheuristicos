import unittest
import numpy as np
import src.core.algorithms.AntColonySystem as ACS
import src.utils.tsp_parser as TSPParser


class ModdifiedAntColonySystem(ACS.AntColonySystem):
    def end_condition(self):
        return round(self.cost(self.best_solution), 4) <= 7544.3659 or self.it >= self.max_iterations


class TravellingSalesmanTest(unittest.TestCase):
    def setUp(self):
        self.seed = 42
        self.default_alpha = 0.1  # 0.1 - 1.0
        self.default_beta = 2.5  # 2 - 5
        self.default_q0 = 0.9  # 0.7 - 0.95
        self.default_colony_size = 50  # 10 - 100
        self.default_iterations = 1000  # 100 - 2000
        self.nodes = TSPParser.parse_tsp_file("./berlin52.tsp")

    def test_colony_size(self):
        for size in range(10, 101, 10):
            with self.subTest(colony_size=size):
                acs = ModdifiedAntColonySystem(self.seed, size, self.default_alpha,
                                               self.default_beta, self.default_q0, self.default_iterations, self.nodes)
                acs.start()

                print(
                    f"iteraciones para llegar al optimo con colony_size={size} costo={acs.cost(acs.best_solution)}: {acs.it}")

    def test_alpha(self):
        for alpha in np.arange(0.1, 1.1, 0.1):
            with self.subTest(alpha=alpha):
                acs = ModdifiedAntColonySystem(self.seed, self.default_colony_size, round(alpha, 1),
                                               self.default_beta, self.default_q0, self.default_iterations, self.nodes)
                acs.start()

                print(
                    f"iteraciones para llegar al optimo con alpha={round(alpha, 1)} costo={acs.cost(acs.best_solution)}: {acs.it}")

    def test_beta(self):
        for beta in np.arange(2.0, 5.5, 0.5):
            with self.subTest(beta=beta):
                acs = ModdifiedAntColonySystem(self.seed, self.default_colony_size, self.default_alpha,
                                               round(beta, 1), self.default_q0, self.default_iterations, self.nodes)
                acs.start()

                print(
                    f"iteraciones para llegar al optimo con beta={round(beta, 1)} costo={acs.cost(acs.best_solution)}: {acs.it}")

    def test_q0(self):
        for q0 in np.arange(0.7, 1.0, 0.05):
            with self.subTest(q0=q0):
                acs = ModdifiedAntColonySystem(self.seed, self.default_colony_size, self.default_alpha,
                                               self.default_beta, round(q0, 2), self.default_iterations, self.nodes)
                acs.start()

                print(
                    f"iteraciones para llegar al optimo con q0={round(q0, 2)} costo={acs.cost(acs.best_solution)}: {acs.it}")


if __name__ == "__main__":
    unittest.main()
