import unittest
import sqlite3
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from src.problems.n_queen.NQueen import NQueen
import os
import itertools


class TestWithElitism(unittest.TestCase):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("db.sqlite", check_same_thread=False)
        self.cur = self.con.cursor()
        
        # Tabla para las semillas (ID = valor de la semilla)
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS seeds (
                ID INTEGER PRIMARY KEY
            )"""
        )
        
        # Tabla para los resultados de experimentos
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS results (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                SEED_ID INTEGER,
                BOARDSIZE INTEGER,
                POPULATIONSIZE INTEGER,
                CROSSOVERRATE REAL,
                MUTATIONRATE REAL,
                ITERATIONS INTEGER,
                FITNESS INTEGER,
                FOREIGN KEY (SEED_ID) REFERENCES seeds(ID)
            )"""
        )
        
        self.db_lock = threading.Lock()
        self._initialize_seeds()
    
    def _initialize_seeds(self):
        """Inicializa las semillas en la tabla seeds si no existen"""
        with self.db_lock:
            # Insertar semillas del 0 al 29 si no existen (ID = valor de semilla)
            for seed_value in range(30):
                self.cur.execute(
                    "INSERT OR IGNORE INTO seeds (ID) VALUES (?)",
                    (seed_value,)
                )
            self.con.commit()

    def run_single_test(self, params):
        """Ejecuta una sola combinación de parámetros"""
        seed, n, population_size, iterations, crossover_rate, mutation_rate = params

        nqueen = NQueen(
            seed,
            n,
            population_size,
            crossover_rate,
            mutation_rate,
            iterations,
        )
        sorted_population = nqueen.start(True)
        fitness_value, _ = sorted_population[0]

        # Usar directamente el valor de la semilla como ID
        return (
            seed,  # seed_id = seed
            n,
            population_size,
            crossover_rate,
            mutation_rate,
            iterations,
            fitness_value,
        )

    def test_n_queen(self):
        # Definir rangos
        ranges = [
            range(30),                 # seeds
            range(4, 31),              # ns
            range(50, 1000, 100),      # population_sizes
            range(100, 1000, 100),     # iterations
            np.arange(0.5, 0.99, 0.1), # crossover_rates
            np.arange(0.01, 0.1, 0.01) # mutation_rates
        ]
        
        # Calcular total sin generar todas las combinaciones
        total_combinations = 1
        for r in ranges:
            total_combinations *= len(r)
        
        print(f"Total de combinaciones a probar: {total_combinations}")
        
        # Usar itertools.product como generador (no convertir a lista)
        parameter_combinations = itertools.product(*ranges)
        
        max_workers = min(os.cpu_count() or 1, 8)  # Limitar a 8 workers para no saturar
        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_params = {
                executor.submit(self.run_single_test, params): params
                for params in parameter_combinations
            }

            completed = 0
            for future in as_completed(future_to_params):
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1

                    # Mostrar progreso cada 100 completados
                    if completed % 100 == 0:
                        print(f"Completados: {completed}/{total_combinations}")

                except Exception as exc:
                    params = future_to_params[future]
                    print(f"Parámetros {params} generaron una excepción: {exc}")

        print("Escribiendo resultados a la base de datos...")
        with self.db_lock:
            self.cur.executemany(
                "INSERT INTO results (SEED_ID, BOARDSIZE, POPULATIONSIZE, CROSSOVERRATE, MUTATIONRATE, ITERATIONS, FITNESS) VALUES (?, ?, ?, ?, ?, ?, ?)",
                results
            )
            self.con.commit()

        print(
            f"Test completado. Se insertaron {len(results)} resultados en la base de datos."
        )
    
    def get_results_with_seeds(self):
        """Método para obtener resultados con los valores de semillas mediante JOIN"""
        with self.db_lock:
            self.cur.execute(
                """SELECT s.ID as SEED_VALUE, r.BOARDSIZE, r.POPULATIONSIZE, r.CROSSOVERRATE, 
                          r.MUTATIONRATE, r.ITERATIONS, r.FITNESS
                   FROM results r
                   JOIN seeds s ON r.SEED_ID = s.ID
                   ORDER BY r.BOARDSIZE, r.POPULATIONSIZE, s.ID"""
            )
            return self.cur.fetchall()


if __name__ == "__main__":
    unittest.main()
