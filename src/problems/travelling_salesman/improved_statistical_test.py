import unittest
import numpy as np
import pandas as pd
import time
import json
from datetime import datetime
import src.core.algorithms.AntColonySystem as ACS
import src.utils.tsp_parser as TSPParser


class OptimalTargetACS(ACS.AntColonySystem):
    """Versión que busca alcanzar el óptimo conocido, como en tu test original"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.optimal_target = 7544.3659  # Valor óptimo verificado
        self.convergence_history = []
        self.execution_time = 0
        self.final_cost = float('inf')
        self.reached_optimal = False
        
    def start(self):
        start_time = time.time()
        self.convergence_history = []
        
        result = super().start()
        
        self.execution_time = time.time() - start_time
        self.final_cost = self.cost(self.best_solution)
        self.reached_optimal = round(self.final_cost, 4) <= self.optimal_target
        
        return result
    
    def end_condition(self):
        # Tu condición original: parar al alcanzar el óptimo O al llegar a max_iterations
        current_cost = self.cost(self.best_solution)
        self.convergence_history.append(current_cost)
        return round(current_cost, 4) <= self.optimal_target or self.it >= self.max_iterations


class StatisticalTSPTest(unittest.TestCase):
    """Test estadísticamente robusto que mantiene tu lógica original"""
    
    def setUp(self):
        self.seed = 42
        self.default_alpha = 0.1
        self.default_beta = 2.5
        self.default_q0 = 0.9
        self.default_colony_size = 50
        self.default_iterations = 1000
        self.nodes = TSPParser.parse_tsp_file("./berlin52.tsp")
        self.optimal_cost = 7544.3659
        self.results = []
        self.runs_per_config = 5  # Número de corridas por configuración
        
    def run_multiple_times(self, params, test_name):
        """Ejecuta múltiples corridas de una configuración"""
        results = []
        
        for run in range(self.runs_per_config):
            # Usar semilla diferente para cada corrida
            seed = self.seed + run
            
            acs = OptimalTargetACS(
                seed=seed,
                colony_size=params['colony_size'],
                alpha=params['alpha'],
                beta=params['beta'],
                q0=params['q0'],
                max_iterations=self.default_iterations,
                nodes=self.nodes
            )
            
            acs.start()
            
            # Calcular gap percentage
            gap_percentage = ((acs.final_cost - self.optimal_cost) / self.optimal_cost) * 100
            
            result = {
                'test_name': test_name,
                'run': run,
                'seed': seed,
                'colony_size': params['colony_size'],
                'alpha': params['alpha'],
                'beta': params['beta'],
                'q0': params['q0'],
                'final_cost': acs.final_cost,
                'execution_time': acs.execution_time,
                'iterations_used': acs.it,
                'reached_optimal': acs.reached_optimal,
                'gap_percentage': gap_percentage,
                'convergence_history': acs.convergence_history.copy(),
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(result)
            self.results.append(result)
            
            # Mensaje como en tu test original, pero con más info
            status = "ÓPTIMO ALCANZADO" if acs.reached_optimal else "MAX ITERACIONES"
            print(f"Run {run+1}/{self.runs_per_config} - {test_name}={params[test_name]} - "
                  f"Iteraciones: {acs.it}, Costo: {acs.final_cost:.4f}, "
                  f"Gap: {gap_percentage:.2f}%, Status: {status}")
        
        return results

    def test_colony_size(self):
        """Test del tamaño de colonia con análisis estadístico"""
        print("\n" + "="*60)
        print("TESTING COLONY SIZE")
        print("="*60)
        
        for size in range(10, 101, 10):
            with self.subTest(colony_size=size):
                params = {
                    'colony_size': size,
                    'alpha': self.default_alpha,
                    'beta': self.default_beta,
                    'q0': self.default_q0,
                    'test_name': 'colony_size'
                }
                
                print(f"\n--- Testing colony_size = {size} ---")
                results = self.run_multiple_times(params, 'colony_size')
                
                # Estadísticas de las corridas
                costs = [r['final_cost'] for r in results]
                iterations = [r['iterations_used'] for r in results]
                reached_optimal_count = sum(r['reached_optimal'] for r in results)
                
                print(f"Estadísticas (n={len(results)}):")
                print(f"  Costo: {np.mean(costs):.2f} ± {np.std(costs):.2f}")
                print(f"  Iteraciones: {np.mean(iterations):.1f} ± {np.std(iterations):.1f}")
                print(f"  Alcanzó óptimo: {reached_optimal_count}/{len(results)} veces")

    def test_alpha(self):
        """Test del parámetro alpha con análisis estadístico"""
        print("\n" + "="*60)
        print("TESTING ALPHA")
        print("="*60)
        
        for alpha in np.arange(0.1, 1.1, 0.1):
            alpha = round(alpha, 1)
            with self.subTest(alpha=alpha):
                params = {
                    'colony_size': self.default_colony_size,
                    'alpha': alpha,
                    'beta': self.default_beta,
                    'q0': self.default_q0,
                    'test_name': 'alpha'
                }
                
                print(f"\n--- Testing alpha = {alpha} ---")
                results = self.run_multiple_times(params, 'alpha')
                
                # Estadísticas de las corridas
                costs = [r['final_cost'] for r in results]
                iterations = [r['iterations_used'] for r in results]
                reached_optimal_count = sum(r['reached_optimal'] for r in results)
                
                print(f"Estadísticas (n={len(results)}):")
                print(f"  Costo: {np.mean(costs):.2f} ± {np.std(costs):.2f}")
                print(f"  Iteraciones: {np.mean(iterations):.1f} ± {np.std(iterations):.1f}")
                print(f"  Alcanzó óptimo: {reached_optimal_count}/{len(results)} veces")

    def test_beta(self):
        """Test del parámetro beta con análisis estadístico"""
        print("\n" + "="*60)
        print("TESTING BETA")
        print("="*60)
        
        for beta in np.arange(2.0, 5.5, 0.5):
            beta = round(beta, 1)
            with self.subTest(beta=beta):
                params = {
                    'colony_size': self.default_colony_size,
                    'alpha': self.default_alpha,
                    'beta': beta,
                    'q0': self.default_q0,
                    'test_name': 'beta'
                }
                
                print(f"\n--- Testing beta = {beta} ---")
                results = self.run_multiple_times(params, 'beta')
                
                # Estadísticas de las corridas
                costs = [r['final_cost'] for r in results]
                iterations = [r['iterations_used'] for r in results]
                reached_optimal_count = sum(r['reached_optimal'] for r in results)
                
                print(f"Estadísticas (n={len(results)}):")
                print(f"  Costo: {np.mean(costs):.2f} ± {np.std(costs):.2f}")
                print(f"  Iteraciones: {np.mean(iterations):.1f} ± {np.std(iterations):.1f}")
                print(f"  Alcanzó óptimo: {reached_optimal_count}/{len(results)} veces")

    def test_q0(self):
        """Test del parámetro q0 con análisis estadístico"""
        print("\n" + "="*60)
        print("TESTING Q0")
        print("="*60)
        
        for q0 in np.arange(0.7, 1.0, 0.05):
            q0 = round(q0, 2)
            with self.subTest(q0=q0):
                params = {
                    'colony_size': self.default_colony_size,
                    'alpha': self.default_alpha,
                    'beta': self.default_beta,
                    'q0': q0,
                    'test_name': 'q0'
                }
                
                print(f"\n--- Testing q0 = {q0} ---")
                results = self.run_multiple_times(params, 'q0')
                
                # Estadísticas de las corridas
                costs = [r['final_cost'] for r in results]
                iterations = [r['iterations_used'] for r in results]
                reached_optimal_count = sum(r['reached_optimal'] for r in results)
                
                print(f"Estadísticas (n={len(results)}):")
                print(f"  Costo: {np.mean(costs):.2f} ± {np.std(costs):.2f}")
                print(f"  Iteraciones: {np.mean(iterations):.1f} ± {np.std(iterations):.1f}")
                print(f"  Alcanzó óptimo: {reached_optimal_count}/{len(results)} veces")

    def tearDown(self):
        """Guarda los resultados al finalizar"""
        if hasattr(self, 'results') and self.results:
            filename = f"statistical_tsp_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            print(f"\n" + "="*60)
            print("RESUMEN FINAL")
            print("="*60)
            print(f"Total de experimentos: {len(self.results)}")
            print(f"Resultados guardados en: {filename}")
            
            # Resumen por parámetro
            df = pd.DataFrame(self.results)
            
            for param in ['colony_size', 'alpha', 'beta', 'q0']:
                if param in df.columns:
                    param_summary = df.groupby(param).agg({
                        'final_cost': ['mean', 'std'],
                        'iterations_used': 'mean',
                        'reached_optimal': 'sum'
                    }).round(2)
                    
                    print(f"\nResumen {param}:")
                    print(param_summary.head())


if __name__ == "__main__":
    # Configurar para que los tests se ejecuten en orden
    suite = unittest.TestSuite()
    
    # Añadir tests en el orden deseado
    suite.addTest(StatisticalTSPTest('test_colony_size'))
    suite.addTest(StatisticalTSPTest('test_alpha'))
    suite.addTest(StatisticalTSPTest('test_beta'))
    suite.addTest(StatisticalTSPTest('test_q0'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)