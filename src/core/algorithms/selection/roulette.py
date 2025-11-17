import numpy as np
import numpy.typing as npt

def roulette(vector_prob: npt.NDArray[np.float64]) -> int:
    suma_total = np.sum(vector_prob)
    valor_aleatorio = np.random.uniform(0, suma_total)
    suma_acumulativa = 0
    for i in range(len(vector_prob)):
        suma_acumulativa += vector_prob[i]
        if suma_acumulativa >= valor_aleatorio:
            return i
    return 0