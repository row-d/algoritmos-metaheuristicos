# Algoritmos Metaheurísticos

Este proyecto implementa varios **algoritmos metaheurísticos** para resolver problemas de optimización combinatoria usando Python. Incluye implementaciones de **Algoritmo Genético** para el problema de las N-Reinas y **Sistema de Colonia de Hormigas (ACS)** para el Problema del Agente Viajero (TSP).

## 🎯 Características

### Algoritmo Genético (N-Reinas)
- ✅ Implementación completa de algoritmo genético
- ✅ Soporte para tableros de cualquier tamaño (N > 3)
- ✅ Visualización del tablero final con las reinas colocadas
- ✅ Parámetros configurables (población, mutación, cruzamiento)
- ✅ Soporte para elitismo
- ✅ Múltiples métodos de selección (ruleta, torneo determinístico/probabilístico)

### Sistema de Colonia de Hormigas (TSP)
- ✅ Implementación del algoritmo ACS (Ant Colony System)
- ✅ Soporte para archivos en formato TSPLIB
- ✅ Parámetros configurables (α, β, q₀, tamaño de colonia)
- ✅ Actualización local y global de feromonas
- ✅ Seguimiento del progreso iteración por iteración

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

El proyecto incluye dos comandos principales: uno para resolver el problema de las N-Reinas usando algoritmos genéticos y otro para resolver el Problema del Agente Viajero usando el Sistema de Colonia de Hormigas.

### 🏃‍♀️ Problema de las N-Reinas (Algoritmo Genético)

#### Comando básico

```bash
python -m src.main n-queen <semilla> <n_reinas> <población> <cruzamiento> <mutación> <generaciones>
```

#### Parámetros

| Parámetro      | Tipo  | Descripción                           | Rango                |
| -------------- | ----- | ------------------------------------- | -------------------- |
| `semilla`      | int   | Semilla para números aleatorios       | Cualquier entero     |
| `n_reinas`     | int   | Número de reinas y tamaño del tablero | > 3                  |
| `población`    | int   | Tamaño de la población por generación | 50-200 (recomendado) |
| `cruzamiento`  | float | Probabilidad de cruzamiento           | 0.0 - 1.0            |
| `mutación`     | float | Probabilidad de mutación              | 0.0 - 1.0            |
| `generaciones` | int   | Número máximo de generaciones         | > 0                  |

#### Ejemplos de uso

##### Problema clásico de 8 reinas

```bash
python -m src.main n-queen 42 8 100 0.8 0.1 1000
```

##### Problema más complejo (15 reinas)

```bash
python -m src.main n-queen 999 15 100 0.99 0.01 500
```

##### Prueba rápida (4 reinas)

```bash
python -m src.main n-queen 123 4 50 0.7 0.2 100
```

#### Interpretación del fitness

- **Fitness = 0**: Solución perfecta
- **Fitness > 0**: Número de pares de reinas que se atacan mutuamente
- **Menor fitness = Mejor solución**

#### Elitismo

Puedes activar el elitismo configurando la variable de entorno `ELITISMO`:

```bash
# Windows
$env:ELITISMO="True"; python -m src.main n-queen 42 8 100 0.8 0.1 1000

# macOS/Linux
export ELITISMO=True
python -m src.main n-queen 42 8 100 0.8 0.1 1000
```

### 🐜 Problema del Agente Viajero (Sistema de Colonia de Hormigas)

#### Comando básico

```bash
python -m src.main acs <archivo> <semilla> <tamaño_colonia> <iteraciones> <alpha> <beta> <q0>
```

#### Parámetros

| Parámetro        | Tipo  | Descripción                                    | Rango recomendado |
| ---------------- | ----- | ---------------------------------------------- | ----------------- |
| `archivo`        | Path  | Archivo con coordenadas en formato TSPLIB     | Archivo válido    |
| `semilla`        | int   | Semilla para números aleatorios               | Cualquier entero  |
| `tamaño_colonia` | int   | Número de hormigas en la colonia              | 10-50             |
| `iteraciones`    | int   | Número máximo de iteraciones                  | 100-1000          |
| `alpha`          | float | Importancia de la feromona (α)                | 0.1-1.0           |
| `beta`           | float | Importancia de la información heurística (β)  | 1.0-5.0           |
| `q0`             | float | Probabilidad de explotación vs exploración    | 0.1-0.9           |

#### Ejemplo de uso

```bash
python -m src.main acs input.txt 42 20 500 0.1 2.0 0.9
```

#### Formato de archivo TSPLIB

El archivo debe seguir el formato estándar TSPLIB:

```
NAME: nombre_problema
TYPE: TSP
COMMENT: descripción
DIMENSION: número_ciudades
EDGE_WEIGHT_TYPE: EUC_2D
NODE_COORD_SECTION
1 x1 y1
2 x2 y2
...
```

## 🏗️ Estructura del proyecto

```
algoritmos-metaheuristicos/
├── src/
│   ├── main.py                    # Punto de entrada del programa
│   ├── commands/
│   │   ├── acs.py                 # Comando para Sistema de Colonia de Hormigas
│   │   └── n_queen.py             # Comando para problema de N-Reinas
│   ├── core/
│   │   ├── EventEmitter.py        # Sistema de eventos
│   │   └── algorithms/
│   │       ├── AntColonySystem.py # Implementación del algoritmo ACS
│   │       └── GeneticAlgo.py     # Implementación del algoritmo genético
│   ├── problems/
│   │   └── n_queen/
│   │       ├── NQueen.py          # Implementación específica del problema
│   │       └── tests/             # Pruebas y análisis
│   └── utils/
│       └── print_chessboard.py    # Utilidades de visualización
├── input.txt                      # Archivo de ejemplo para TSP (Berlin52)
└── requirements.txt               # Dependencias del proyecto
```

## 📊 Algoritmos Implementados

### 1. Algoritmo Genético

**Problema:** N-Reinas

**Descripción:** Encuentra una configuración de N reinas en un tablero NxN donde ninguna reina puede atacar a otra.

**Características especiales:**
- Representación por permutaciones
- Crossover de orden (OX)
- Mutación por intercambio
- Soporte para elitismo
- Múltiples métodos de selección

### 2. Sistema de Colonia de Hormigas (ACS)

**Problema:** Problema del Agente Viajero (TSP)

**Descripción:** Encuentra el camino más corto que visita todas las ciudades exactamente una vez y regresa al punto de origen.

**Características especiales:**
- Actualización local y global de feromonas
- Regla de transición pseudo-aleatoria proporcional
- Información heurística basada en distancia
- Balance entre explotación y exploración

## 🔬 Ejemplos de Resultados

### N-Reinas (8x8)
```
┌───┬───┬───┬───┬───┬───┬───┬───┐
│   │ ♛ │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │ ♛ │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │ ♛ │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │   │ ♛ │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │ ♛ │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♛ │   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │ ♛ │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │ ♛ │   │
└───┴───┴───┴───┴───┴───┴───┴───┘
Fitness: 0 (Solución perfecta)
```

## 📚 Referencias

- Dorigo, M., & Gambardella, L. M. (1997). Ant colony system: a cooperative learning approach to the traveling salesman problem.
- Holland, J. H. (1992). Adaptation in natural and artificial systems.
- Reinelt, G. (1991). TSPLIB—A traveling salesman problem library.
