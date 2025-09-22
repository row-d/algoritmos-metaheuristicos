import unittest
import sqlite3
import numpy as np
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import sys
import os
import itertools

from src.problems.n_queen.NQueen import NQueen


class TestWithElitism(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
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
                GENERATIONS_EXECUTED INTEGER,
                ELITISMO INTEGER DEFAULT 1,
                FOREIGN KEY (SEED_ID) REFERENCES seeds(ID)
            )"""
        )
        
        # Tabla para almacenar poblaciones finales
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS populations (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                RESULT_ID INTEGER,
                INDIVIDUAL TEXT,
                FITNESS INTEGER,
                RANK_IN_POPULATION INTEGER,
                FOREIGN KEY (RESULT_ID) REFERENCES results(ID)
            )"""
        )
        
        self.db_lock = threading.Lock()
        self._initialize_seeds()
    
    def _initialize_seeds(self):
        """Inicializa las semillas en la tabla seeds si no existen"""
        with self.db_lock:
            # Insertar semillas del 0 al 29 si no existen (ID = valor de semilla)
            for seed_value in range(1, 11):  # Reducido a 10 semillas para menos memoria
                self.cur.execute(
                    "INSERT OR IGNORE INTO seeds (ID) VALUES (?)",
                    (seed_value,)
                )
            self.con.commit()

    def run_single_test(self, params):
        """Ejecuta una sola combinación de parámetros y guarda inmediatamente"""
        seed, n, population_size, iterations, crossover_rate, mutation_rate, elitismo = params

        nqueen = NQueen(
            seed,
            n,
            population_size,
            crossover_rate,
            mutation_rate,
            iterations,
        )
        sorted_population = nqueen.start(elitismo)
        fitness_value, _ = sorted_population[0]

        # Guardar resultado inmediatamente para evitar acumulación en memoria
        with self.db_lock:
            self.cur.execute(
                "INSERT INTO results (SEED_ID, BOARDSIZE, POPULATIONSIZE, CROSSOVERRATE, MUTATIONRATE, ITERATIONS, FITNESS, GENERATIONS_EXECUTED, ELITISMO) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (seed, n, population_size, crossover_rate, mutation_rate, iterations, fitness_value, nqueen.gen, int(elitismo))
            )
            result_id = self.cur.lastrowid
            
            # Guardar solo los mejores 10 individuos de la población para ahorrar memoria
            top_individuals = sorted_population[:10]
            population_data = [
                (result_id, json.dumps(individual), fitness, rank)
                for rank, (fitness, individual) in enumerate(top_individuals, 1)
            ]
            
            self.cur.executemany(
                "INSERT INTO populations (RESULT_ID, INDIVIDUAL, FITNESS, RANK_IN_POPULATION) VALUES (?, ?, ?, ?)",
                population_data
            )
            self.con.commit()

        # Retornar solo información básica (no la población completa)
        return result_id

    def test_n_queen(self):
        # Rangos reducidos para evitar exceso de memoria
        ranges = [
            range(1, 11),              # seeds (10 semillas)
            range(4, 16),              # ns (tableros 4x4 a 15x15)
            range(50, 151, 50),        # population_sizes (50, 100, 150)
            range(100, 501, 200),      # iterations (100, 300, 500)
            np.arange(0.6, 0.91, 0.1), # crossover_rates (reducido)
            np.arange(0.01, 0.06, 0.02), # mutation_rates (reducido)
            [False]                    # elitismo (solo SIN elitismo, ya que los tests CON elitismo ya están hechos)
        ]
        
        # Calcular total sin generar todas las combinaciones
        total_combinations = 1
        for r in ranges:
            total_combinations *= len(r)
        
        print(f"Total de combinaciones a probar: {total_combinations}")
        
        # Usar itertools.product como generador (no convertir a lista)
        parameter_combinations = itertools.product(*ranges)
        
        max_workers = min(os.cpu_count() or 1, 4)  # Reducido a 4 workers para menos memoria
        
        completed_count = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Procesar en lotes para evitar acumulación de memoria
            batch_size = 20  # Procesar 20 combinaciones a la vez
            batch = []
            
            for params in parameter_combinations:
                batch.append(params)
                
                if len(batch) >= batch_size:
                    # Procesar el lote actual
                    futures = [executor.submit(self.run_single_test, p) for p in batch]
                    
                    for future in as_completed(futures):
                        try:
                            result_id = future.result()
                            completed_count += 1
                            
                            # Mostrar progreso cada 10 completados
                            if completed_count % 10 == 0:
                                print(f"Completados: {completed_count}/{total_combinations}")
                                
                        except Exception as exc:
                            print(f"Error en ejecución: {exc}")
                    
                    # Limpiar el lote
                    batch = []
            
            # Procesar el último lote si queda algo
            if batch:
                futures = [executor.submit(self.run_single_test, p) for p in batch]
                
                for future in as_completed(futures):
                    try:
                        result_id = future.result()
                        completed_count += 1
                        
                        if completed_count % 10 == 0:
                            print(f"Completados: {completed_count}/{total_combinations}")
                            
                    except Exception as exc:
                        print(f"Error en ejecución: {exc}")

        print(f"Test completado. Se procesaron {completed_count} combinaciones en total.")
    
    def get_results_with_seeds(self):
        """Método para obtener resultados con los valores de semillas mediante JOIN"""
        with self.db_lock:
            self.cur.execute(
                """SELECT s.ID as SEED_VALUE, r.BOARDSIZE, r.POPULATIONSIZE, r.CROSSOVERRATE, 
                          r.MUTATIONRATE, r.ITERATIONS, r.FITNESS, r.GENERATIONS_EXECUTED, r.ELITISMO
                   FROM results r
                   JOIN seeds s ON r.SEED_ID = s.ID
                   ORDER BY r.BOARDSIZE, r.POPULATIONSIZE, s.ID"""
            )
            return self.cur.fetchall()
    
    def get_population_data(self, result_id=None):
        """Método para obtener datos de población"""
        with self.db_lock:
            if result_id:
                self.cur.execute(
                    """SELECT r.ID as RESULT_ID, r.SEED_ID, r.BOARDSIZE, r.POPULATIONSIZE,
                              p.INDIVIDUAL, p.FITNESS, p.RANK_IN_POPULATION
                       FROM results r
                       JOIN populations p ON r.ID = p.RESULT_ID
                       WHERE r.ID = ?
                       ORDER BY p.RANK_IN_POPULATION""",
                    (result_id,)
                )
            else:
                self.cur.execute(
                    """SELECT r.ID as RESULT_ID, r.SEED_ID, r.BOARDSIZE, r.POPULATIONSIZE,
                              p.INDIVIDUAL, p.FITNESS, p.RANK_IN_POPULATION
                       FROM results r
                       JOIN populations p ON r.ID = p.RESULT_ID
                       ORDER BY r.ID, p.RANK_IN_POPULATION"""
                )
            return self.cur.fetchall()
    
    def get_best_solutions(self, board_size=None):
        """Método para obtener las mejores soluciones (fitness = 0)"""
        with self.db_lock:
            if board_size:
                self.cur.execute(
                    """SELECT r.ID, r.SEED_ID, r.BOARDSIZE, r.POPULATIONSIZE, r.FITNESS, 
                              r.GENERATIONS_EXECUTED, r.ELITISMO, p.INDIVIDUAL
                       FROM results r
                       JOIN populations p ON r.ID = p.RESULT_ID
                       WHERE r.FITNESS = 0 AND r.BOARDSIZE = ? AND p.RANK_IN_POPULATION = 1
                       ORDER BY r.GENERATIONS_EXECUTED""",
                    (board_size,)
                )
            else:
                self.cur.execute(
                    """SELECT r.ID, r.SEED_ID, r.BOARDSIZE, r.POPULATIONSIZE, r.FITNESS, 
                              r.GENERATIONS_EXECUTED, r.ELITISMO, p.INDIVIDUAL
                       FROM results r
                       JOIN populations p ON r.ID = p.RESULT_ID
                       WHERE r.FITNESS = 0 AND p.RANK_IN_POPULATION = 1
                       ORDER BY r.BOARDSIZE, r.GENERATIONS_EXECUTED"""
                )
            return self.cur.fetchall()
    
    def get_elitism_comparison(self, board_size=None):
        """Método para comparar resultados con y sin elitismo"""
        with self.db_lock:
            if board_size:
                self.cur.execute(
                    """SELECT 
                        ELITISMO,
                        COUNT(*) as total_experiments,
                        COUNT(CASE WHEN FITNESS = 0 THEN 1 END) as perfect_solutions,
                        AVG(FITNESS) as avg_fitness,
                        MIN(FITNESS) as best_fitness,
                        AVG(GENERATIONS_EXECUTED) as avg_generations,
                        MIN(GENERATIONS_EXECUTED) as min_generations
                    FROM results 
                    WHERE BOARDSIZE = ?
                    GROUP BY ELITISMO 
                    ORDER BY ELITISMO DESC""",
                    (board_size,)
                )
            else:
                self.cur.execute(
                    """SELECT 
                        ELITISMO,
                        COUNT(*) as total_experiments,
                        COUNT(CASE WHEN FITNESS = 0 THEN 1 END) as perfect_solutions,
                        AVG(FITNESS) as avg_fitness,
                        MIN(FITNESS) as best_fitness,
                        AVG(GENERATIONS_EXECUTED) as avg_generations,
                        MIN(GENERATIONS_EXECUTED) as min_generations
                    FROM results 
                    GROUP BY ELITISMO 
                    ORDER BY ELITISMO DESC"""
                )
            return self.cur.fetchall()


if __name__ == "__main__":
    unittest.main()
