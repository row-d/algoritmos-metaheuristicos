# Optimizaciones Realizadas para Reducir Consumo de Memoria

## Cambios Implementados

### 1. **Nueva Tabla de Poblaciones**
- Se agregó la tabla `populations` para almacenar datos de las poblaciones finales
- Solo se guardan los **10 mejores individuos** de cada experimento (en lugar de toda la población)
- Se incluye el ranking de cada individuo en la población

### 2. **Escritura Inmediata a Base de Datos**
- Los resultados se escriben **inmediatamente** después de cada experimento
- Se eliminó la acumulación de todos los resultados en memoria
- Cada resultado se guarda en la BD tan pronto como se completa

### 3. **Procesamiento en Lotes**
- Los experimentos se procesan en **lotes de 20** combinaciones
- Esto evita la acumulación excesiva de futures y reduce el uso de memoria
- Se limpia la memoria entre lotes

### 4. **Reducción de Parámetros**
- **Semillas**: Reducidas de 30 a 10 (range(1, 11))
- **Tamaños de tablero**: Reducidos de 4-30 a 4-15 (range(4, 16))
- **Tamaños de población**: Reducidos a 3 valores (50, 100, 150)
- **Iteraciones**: Reducidas a 3 valores (100, 300, 500)
- **Crossover rates**: Reducidas de 49 a 4 valores
- **Mutation rates**: Reducidas de 9 a 3 valores

### 6. **Campo de Elitismo Agregado**
- Se agregó la columna `ELITISMO` con valor por defecto 1 (TRUE)
- Permite comparar experimentos con y sin elitismo
- Los experimentos previos quedan marcados automáticamente como "con elitismo"
- **Estrategia actual**: Solo ejecutar nuevos tests SIN elitismo para completar la comparación

### 7. **Límite de Workers**
- Reducido de 8 a **4 workers máximo** para el ThreadPoolExecutor
- Esto reduce la carga simultánea de memoria

### 8. **Campos Adicionales**
- Se agregó `GENERATIONS_EXECUTED` para tracking del número de generaciones
- Se agregó `ELITISMO` para distinguir entre experimentos con y sin elitismo
- Mejor información para análisis posterior y comparaciones

## Estructura de Base de Datos

### Tabla `results`
```sql
- ID (PK)
- SEED_ID
- BOARDSIZE
- POPULATIONSIZE
- CROSSOVERRATE
- MUTATIONRATE
- ITERATIONS
- FITNESS
- GENERATIONS_EXECUTED  (NUEVO)
- ELITISMO INTEGER DEFAULT 1  (NUEVO)
```

### Tabla `populations` (NUEVA)
```sql
- ID (PK)
- RESULT_ID (FK -> results.ID)
- INDIVIDUAL (JSON string)
- FITNESS
- RANK_IN_POPULATION
```

## Métodos de Consulta Nuevos

### `get_population_data(result_id=None)`
- Obtiene datos de población para un resultado específico o todos
- Permite analizar los mejores individuos de cada experimento

### `get_best_solutions(board_size=None)`
- Obtiene solo las soluciones perfectas (fitness = 0)
- Filtra por tamaño de tablero opcionalmente

### `get_elitism_comparison(board_size=None)`
- Compara resultados entre experimentos con y sin elitismo
- Muestra estadísticas de éxito, fitness promedio y generaciones por tipo

## Estimación de Reducción de Memoria

**Antes:**
- ~1.3 millones de combinaciones
- Todas almacenadas en memoria hasta el final
- Poblaciones completas en memoria
- **Estimado: 8+ GB RAM**

**Después:**
- ~7,200 combinaciones sin elitismo (para completar la comparación)
- ~12,960 combinaciones con elitismo (ya completadas)
- **Total final**: ~20,160 combinaciones
- Escritura inmediata a BD (sin acumulación)
- Solo 10 mejores individuos por experimento
- Procesamiento en lotes de 20
- **Estimado para nuevos tests**: <500 MB RAM

## Uso del Nuevo Sistema

```python
# Ejecutar test optimizado con comparación de elitismo
test = TestWithElitism()
test.test_n_queen()

# Consultar resultados
results = test.get_results_with_seeds()
best_solutions = test.get_best_solutions()
population_data = test.get_population_data(result_id=1)

# Comparar elitismo vs no-elitismo
elitism_comparison = test.get_elitism_comparison()
elitism_comparison_8x8 = test.get_elitism_comparison(board_size=8)
```

## Archivos Incluidos

1. **test_with_etilism.py** - Test principal modificado
2. **test_example.py** - Script de ejemplo para ejecutar y consultar resultados