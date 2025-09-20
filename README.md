# Algoritmos Metaheurísticos - Problema de las N-Reinas

Este proyecto implementa un **algoritmo genético** para resolver el clásico **problema de las N-Reinas** usando Python. El objetivo es colocar N reinas en un tablero de ajedrez NxN de tal manera que ninguna reina pueda atacar a otra.

## 🎯 Características

- ✅ Implementación completa de algoritmo genético
- ✅ Soporte para tableros de cualquier tamaño (N > 3)
- ✅ Visualización del tablero final con las reinas colocadas
- ✅ Parámetros configurables (población, mutación, cruzamiento)
- ✅ Interfaz de línea de comandos amigable
- ✅ Seguimiento del progreso generación por generación

## 🚀 Instalación

### Prerrequisitos

- **Python 3.8+** instalado en tu sistema
- **pip** (incluido con Python)

### 1. Clonar el repositorio

```bash
git clone https://github.com/row-d/algoritmos-metaheuristicos.git
cd algoritmos-metaheuristicos
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Comando básico

```bash
python -m src.main <semilla> <n_reinas> <población> <cruzamiento> <mutación> <generaciones>
```

### Parámetros

| Parámetro      | Tipo  | Descripción                           | Rango                |
| -------------- | ----- | ------------------------------------- | -------------------- |
| `semilla`      | int   | Semilla para números aleatorios       | Cualquier entero     |
| `n_reinas`     | int   | Número de reinas y tamaño del tablero | > 3                  |
| `población`    | int   | Tamaño de la población por generación | 50-200 (recomendado) |
| `cruzamiento`  | float | Probabilidad de cruzamiento           | 0.0 - 1.0            |
| `mutación`     | float | Probabilidad de mutación              | 0.0 - 1.0            |
| `generaciones` | int   | Número máximo de generaciones         | > 0                  |

### Ejemplos de uso

#### Problema clásico de 8 reinas

```bash
python -m src.main 42 8 100 0.8 0.1 1000
```

#### Problema más complejo (15 reinas)

```bash
python -m src.main 999 15 100 0.99 0.01 500
```

#### Prueba rápida (4 reinas)

```bash
python -m src.main 123 4 50 0.7 0.2 100
```

### Interpretación del fitness

- **Fitness = 0**: Solución perfecta
- **Fitness > 0**: Número de pares de reinas que se atacan mutuamente
- **Menor fitness = Mejor solución**

### Elitismo

Puedes activar el elitismo configurando la variable de entorno `ELITISMO`:

```bash
# Windows
$env:ELITISMO="True";
python -m src.main 42 8 100 0.8 0.1 1000

# macOS/Linux
export ELITISMO=True
python -m src.main 42 8 100 0.8 0.1 1000
```

## 🏗️ Estructura del proyecto

```
algoritmos-metaheuristicos/
├── src/
│   ├── main.py                    # Punto de entrada del programa
│   ├── core/
│   │   ├── EventEmitter.py        # Sistema de eventos
│   │   └── algorithms/
│   │       └── GeneticAlgo.py     # Implementación del algoritmo genético
│   ├── problems/
│   │   └── n_queen/
│   │       ├── NQueen.py          # Implementación específica del problema
│   │       └── tests/
│   └── utils/
│       └── print_chessboard.py    # Utilidades de visualización
└── requirements.txt               # Dependencias del proyecto
```
