import sys
from NQueen import NQueen


def main():
    if len(sys.argv) > 1:
        seed = float(sys.argv[1])
        n = int(sys.argv[2])
        population_size = int(sys.argv[3])
        crossover_rate = float(sys.argv[4])
        mutation_rate = float(sys.argv[5])
        iterations = int(sys.argv[6])

        nqueen = NQueen(
            seed, n, population_size, crossover_rate, mutation_rate, iterations
        )
        nqueen.start()

    else:
        print(
            "Usage: python main.py <seed> <n> <population_size> <crossover_rate> <mutation_rate> <iterations>"
        )
        print("Example: python main.py 42 8 100 0.7 0.01 1000")
        sys.exit(1)


if __name__ == "__main__":
    main()
