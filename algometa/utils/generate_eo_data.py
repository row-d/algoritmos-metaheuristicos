from __future__ import annotations
from pathlib import Path
from typing import Sequence, Callable, Iterable, Union, List, TypeAlias, cast
import csv
import numpy as np
from joblib import Parallel, delayed, parallel  # type: ignore
from contextlib import contextmanager
from tqdm import tqdm
from algometa.core.algorithms.ExtremeOptimization import ExtremeOptimization
from algometa.utils.knapack_parser import KnapdackData

# Alias explícitos de tipos
KnapInstance: TypeAlias = KnapdackData
InstanceInput: TypeAlias = Union[Callable[[], KnapInstance], KnapInstance]
Row: TypeAlias = List[Union[str, int, float]]


def _run_task(seed: int, tau: float, iterations: int, inst: KnapInstance) -> Row:
    eo = ExtremeOptimization(
        seed=seed,
        n_items=inst['n'],
        capacidad=inst['c'],
        precios=np.array(inst['precios']),
        pesos=np.array(inst['pesos']),
        tau=tau,
        max_iterations=iterations,
        optimal_solution=inst['z']
    )
    _, best_value = eo.start()
    return [
        inst['title'],
        inst['n'],
        inst['c'],
        iterations,
        seed,
        tau,
        eo.iterations,
        best_value,
        inst['z']
    ]


def _materialize(instances: Sequence[InstanceInput]) -> List[KnapInstance]:
    materialized: List[KnapInstance] = []
    for x in instances:
        materialized.append(x() if callable(x) else x)
    return materialized


def generate_data(
    instances: Sequence[InstanceInput],
    filename: Path,
    seeds: Iterable[int] | None = None,
    tau_values: Iterable[float] | None = None,
    iteration_values: Iterable[int] | None = None,
    n_jobs: int = -1,
    verbose: int = 0,
    show_progress: bool = True
) -> None:
    """Genera datos aplicando Extreme Optimization sobre cada instancia.

    Simplificado para uso fuera de notebook:
    - Paralelización vía joblib (backend loky para procesos).
    - Instancias pueden ser dicts ya parseados o callables que retornan dict.
    - Escribe por instancia (lista en memoria manejable: 10*11*10=1100 filas por instancia).
    """
    seeds = seeds or range(1, 2)
    tau_values = tau_values or np.arange(1.0, 2.1, 0.2)
    iteration_values = iteration_values or range(500, 1001, 500)

    insts: List[KnapInstance] = _materialize(instances)

    headers = [
        'instance', 'n_items', 'capacity', 'max_iterations',
        'seed', 'tau', 'iterations', 'best_value', 'optimal_value'
    ]

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        total_per_instance = len(list(seeds)) * len(list(tau_values)) * len(list(iteration_values))

        @contextmanager
        def tqdm_joblib(tqdm_obj):  # type: ignore[valid-type]
            """Integración ligera de tqdm con joblib para progreso por batch."""
            class TqdmBatchCallback(parallel.BatchCompletionCallBack):  # type: ignore
                def __call__(self, *args, **kwargs):  # type: ignore[override]
                    tqdm_obj.update(n=self.batch_size)  # type: ignore[attr-defined]
                    return super().__call__(*args, **kwargs)
            old_cb = parallel.BatchCompletionCallBack
            parallel.BatchCompletionCallBack = TqdmBatchCallback
            try:
                yield
            finally:
                parallel.BatchCompletionCallBack = old_cb
                tqdm_obj.close()  # type: ignore[attr-defined]

        for inst in insts:
            tasks_list = [
                (seed, float(tau), it) for seed in seeds
                for tau in tau_values for it in iteration_values
            ]
            delayed_calls = [delayed(_run_task)(seed, tau, it, inst) for seed, tau, it in tasks_list]
            if show_progress:
                with tqdm_joblib(tqdm(total=total_per_instance, desc=inst['title'])):
                    rows_raw = Parallel(n_jobs=n_jobs, backend='loky', verbose=verbose)(delayed_calls)
            else:
                rows_raw = Parallel(n_jobs=n_jobs, backend='loky', verbose=verbose)(delayed_calls)
            writer.writerows(cast(List[Row], rows_raw))
    print(f"Data saved to {filename.absolute()}")

__all__ = ["generate_data"]
