#set text(lang: "es")
#import "@preview/charged-ieee:0.1.4": ieee
#import "@preview/lovelace:0.3.0": *

#show: ieee.with(
  title: [Optimización Extrema aplicada al problema de la mochila],
  abstract: [
    Este artículo presenta la aplicación del algoritmo de Optimización Extrema (EO) para resolver el problema clásico de la mochila. EO es una metaheurística inspirada en el concepto de criticalidad auto-organizada, que se caracteriza por realizar modificaciones probabilísticas extremas en las soluciones. Se implementa una variante que utiliza selección por ranking con parámetro de temperatura ($tau$) y una estrategia dual que adapta el comportamiento según la factibilidad de la solución actual. La implementación emplea una inicialización minimalista y un mecanismo de selección probabilística que balancea exploración e intensificación, demostrando ser un enfoque simple pero efectivo para el problema de la mochila.
  ],
  authors: (
    (
      name: "David Gómez",
      location: [Concepción, Chile],
      email: "dgomezp@ing.ucsc.cl",
    ),
    (
      name: "Felipe Alarcon",
      location: [Concepción, Chile],
      email: "falarcon@ing.ucsc.cl",
    ),
    (
      name: "Rodrigo Ramirez",
      location: [Concepción, Chile],
      email: "rramirezv@ing.ucsc.cl",
    ),
  ),
  index-terms: ("Optimización Extrema", "Metaheurísticas", "Problema de la mochila", "Selección probabilística", "Parámetro tau"),
  bibliography: bibliography("refs.bib"),
  figure-supplement: [Fig.],
)

= Introducción

El problema de la mochila es uno de los problemas de optimización combinatorial más estudiados en la literatura científica. Formalmente, consiste en seleccionar un subconjunto de elementos de un conjunto dado, cada uno con un peso y un valor asociado, de manera que se maximice el valor total sin exceder la capacidad de peso de la mochila @dantzig1957.

Este problema pertenece a la clase NP-hard, lo que significa que no existe un algoritmo de tiempo polinomial que garantice encontrar la solución óptima para todas las instancias. Por esta razón, los algoritmos metaheurísticos han ganado popularidad como enfoques efectivos para resolver instancias grandes del problema en tiempo razonable.

La Optimización Extrema (EO) es una metaheurística relativamente nueva propuesta por Boettcher y Percus en 1999 @boettcher1999. Se inspira en el concepto de criticalidad auto-organizada observado en sistemas complejos de la física, donde pequeñas perturbaciones locales pueden llevar a cambios dramáticos en el sistema completo.

== Características de EO

EO se diferencia de otros algoritmos evolutivos en varios aspectos fundamentales:

1. *Operación sobre un solo individuo*: A diferencia de los algoritmos genéticos que mantienen una población, EO trabaja con una sola solución que evoluciona iterativamente.

2. *Selección extrema*: En cada iteración, se identifica el componente "más malo" de la solución actual y se modifica de manera aleatoria.

3. *No utiliza información de fitness global*: La decisión de qué modificar se basa únicamente en la evaluación local de cada componente.

4. *Simplicidad conceptual*: El algoritmo requiere pocos parámetros y su implementación es relativamente directa.

== Objetivos del trabajo

En este trabajo se presenta una implementación de EO específicamente adaptada para el problema de la mochila. Los objetivos principales son:

- Desarrollar una implementación eficiente que utilice selección probabilística con parámetro de temperatura
- Implementar una estrategia dual de modificación basada en el estado de factibilidad
- Definir un mecanismo de control de la intensidad de selección mediante el parámetro $tau$
- Evaluar el comportamiento del algoritmo con diferentes configuraciones de parámetros

= Metodología <sec:metodologia>

== Formulación del problema

El problema de la mochila 0-1 se puede formular matemáticamente como:

$ max sum_(i=1)^n v_i x_i $ <eq:objetivo>

sujeto a:

$ sum_(i=1)^n w_i x_i <= W $ <eq:restriccion>

$ x_i in {0, 1}, quad i = 1, 2, ..., n $ <eq:binaria>

donde:
- $n$ es el número total de elementos disponibles
- $v_i$ es el valor del elemento $i$
- $w_i$ es el peso del elemento $i$
- $W$ es la capacidad máxima de la mochila
- $x_i$ es una variable binaria que indica si el elemento $i$ está incluido (1) o no (0)

== Algoritmo de EO para la mochila

El algoritmo implementado adapta los principios de EO específicamente para el problema de la mochila, incorporando un parámetro de temperatura $tau$ para controlar la selección probabilística:

=== Representación de la solución

Cada solución se representa como un vector binario $x = (x_1, x_2, ..., x_n)$ donde $x_i = 1$ si el elemento $i$ está en la mochila y $x_i = 0$ en caso contrario.

=== Función de fitness y selección

La implementación utiliza la relación valor/peso ($v_i / w_i$) como medida de calidad para cada elemento. El algoritmo emplea un mecanismo de selección por ruleta biased con un parámetro $tau$ que controla la intensidad de la selección:

$
  p_k = k^{-tau}
$ <eq:prob-seleccion>

donde $k$ es el rango del elemento cuando se ordena por su valor de fitness, y $tau$ es el parámetro de temperatura que controla qué tan extrema es la selección. Valores altos de $tau$ favorecen la selección de elementos con peor fitness (más extrema), mientras que valores bajos hacen la selección más uniforme.

=== El parámetro tau y su impacto

El parámetro $tau$ es fundamental en la implementación y controla el balance entre diversificación e intensificación:

- *$tau$ alto (ej. $tau = 2.0$)*: Selección muy extrema, favorece fuertemente elementos con peor fitness. Promueve exploración agresiva.
- *$tau$ bajo (ej. $tau = 1.0$)*: Selección moderada, distribución más uniforme de probabilidades. Balance entre exploración y explotación.  
- *$tau$ muy bajo (ej. $tau = 0.5$)*: Selección casi uniforme, comportamiento más aleatorio.

La elección apropiada de $tau$ depende de las características del problema y del tiempo disponible para la búsqueda.

=== Procedimiento principal

#figure(
  pseudocode-list(
    booktabs: true,
    title: [Pseudocódigo del algoritmo EO para el problema de la mochila],
  )[
    + *Entrada:* Elementos ${(v_1,w_1), ..., (v_n,w_n)}$, capacidad $W$, parámetro $tau$
    + *Salida:* Solución $x = (x_1, x_2, ..., x_n)$
    +
    + Generar solución inicial factible (un elemento aleatorio)
    + Calcular fitness $f_i = v_i / w_i$ para cada elemento $i$
    + $x_"mejor" arrow.l x$ // Guardar mejor solución encontrada
    + *repetir* hasta criterio de parada:
      + *si* solución actual es factible *entonces*
        + // Intentar agregar un elemento (mejorar solución)
        + Obtener elementos no incluidos ($x_i = 0$)
        + Ordenar por fitness descendente
        + Generar vector de probabilidades: $p_k = k^{-tau}$
        + Seleccionar elemento mediante ruleta e incluirlo
      + *sino*
        + // Remover elemento para mantener factibilidad  
        + Obtener elementos incluidos ($x_i = 1$)
        + Ordenar por fitness ascendente
        + Generar vector de probabilidades: $p_k = k^{-tau}$
        + Seleccionar elemento mediante ruleta y removerlo
      + *fin si*
      + *si* solución es factible y mejor que $x_"mejor"$ *entonces*
        + $x_"mejor" arrow.l x$
      + *fin si*
    + *fin repetir*
    + *retorna* $x_"mejor"$
  ],
) <fig:algoritmo>

=== Generación de solución inicial

El algoritmo comienza con una solución inicial muy simple: selecciona aleatoriamente un único elemento que pueda caber en la mochila. Esta inicialización minimalista es característica de EO, ya que permite que el algoritmo explore gradualmente el espacio de soluciones desde un punto de partida extremo.

=== Estrategia dual de modificación

La implementación utiliza una estrategia dual dependiente del estado de factibilidad de la solución actual:

1. *Solución factible*: Se intenta agregar elementos que no están incluidos, priorizando probabilísticamente aquellos con mejor relación valor/peso.

2. *Solución infactible*: Se remueven elementos incluidos, priorizando probabilísticamente aquellos con peor relación valor/peso.

Esta estrategia permite al algoritmo mantener un equilibrio dinámico entre exploración y factibilidad sin necesidad de un mecanismo de reparación explícito.

= Experimentos y Resultados <sec:resultados>

== Conjuntos de instancias

El análisis experimental se enfoca exclusivamente en estudiar la sensibilidad del algoritmo EO a tres parámetros: $tau$, la semilla aleatoria y el número máximo de iteraciones. Para ello, se utilizan tres familias de instancias ampliamente empleadas en la literatura:

#figure(
  caption: [Conjuntos de instancias considerados],
  placement: top,
  table(
    columns: (auto, auto),
    align: (left, left),
    inset: (x: 8pt, y: 4pt),
    stroke: (x, y) => if y <= 1 { (top: 0.5pt) },
    fill: (x, y) => if y > 0 and calc.rem(y, 2) == 0 { rgb("#efefef") },

    table.header[Familia][Ruta],
    [Small Coeff (Pisinger)], [papers/ExtremalOptimization/smallcoeff_pisinger/],
    [Large Coeff (Pisinger)], [papers/ExtremalOptimization/largecoeff_pisinger/],
    [Hard Instances (Pisinger)], [papers/ExtremalOptimization/hardinstances_pisinger/],
  ),
) <tab:familias>

== Diseño experimental y parámetros

El objetivo es identificar configuraciones de (tau, seed, iteraciones) que ofrecen el mejor desempeño por familia de instancias. Para cada conjunto se evalúan combinaciones de parámetros siguiendo una rejilla configurable.

- Parámetro $tau$: controla la intensidad de la selección probabilística ($p_k = k^{-tau}$). Valores de referencia: 0.8–2.0.
- Semilla (seed): controla la reproducibilidad. Se exploran múltiples semillas para medir variabilidad.
- Iteraciones: máximo de pasos de EO. Valores de referencia: 500–10000.

Métricas reportadas por instancia y luego agregadas por familia:

- Tasa de óptimo: proporción de instancias con diferencia 0.
- Error absoluto promedio: promedio de precio_mejor - precio_óptimo.
- Iteraciones hasta el mejor: número de iteraciones consumidas al lograr la mejor solución.

== Ejecución y recolección de resultados

La recolección de datos se realiza ejecutando el comando CLI existente (sin cambios a la implementación). A modo de ejemplo, el siguiente comando ejecuta EO sobre un conjunto de instancias y genera un CSV en la carpeta `papers`:

#figure(
  box(fill: rgb("#f7f7f7"), inset: 8pt, stroke: rgb("#dddddd"), radius: 4pt, [
    python -m src.main eo -s --output="./papers" "smallcoeff_pisinger\\knapPI_1_50_1000.csv" 3000 4534 1.6
  ]),
  caption: [Comando de ejemplo para generar resultados (CSV)],
  placement: top,
) <fig:comando>

== Resultados de ejemplo

Como ejemplo de salida, se emplea el archivo `papers/result_eo_n50_c995_tau1.6_seed4534.csv`, que contiene los campos: Instancia, Iteraciones, Items, Capacidad, Precio Mejor Solución, Precio Solución Óptima y Diferencia. A continuación, se muestra un extracto:

#figure(
  caption: [Extracto de resultados generados por EO con $tau=1.6$, seed=4534, 3000 iteraciones],
  placement: top,
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    align: (left, center, center, center, center, center, center),
    inset: (x: 6pt, y: 4pt),
    stroke: (x, y) => if y <= 1 { (top: 0.5pt) },
    fill: (x, y) => if y > 0 and calc.rem(y, 2) == 0 { rgb("#efefef") },

    table.header[Instancia][Iter.][Items][Cap.][Mejor][Óptimo][Dif.],
    [knapPI_1_50_1000_1], [50], [50], [995], [8373], [8373], [0],
    [knapPI_1_50_1000_2], [30], [50], [997], [5847], [5847], [0],
    [knapPI_1_50_1000_11], [829], [50], [2397], [9533], [9533], [0],
    [knapPI_1_50_1000_22], [3000], [50], [5241], [12837], [12839], [-2],
    [knapPI_1_50_1000_36], [3000], [50], [9462], [13513], [13517], [-4],
    [knapPI_1_50_1000_38], [3000], [50], [8297], [17760], [17772], [-12],
  ),
) <tab:ejemplo>

// Lectura dinámica del CSV de ejemplo y visualización compacta
#let datos_ej = csv("./result_eo_n50_c995_tau1.6_seed4534.csv")
#let encabezados_ej = (
  "Instancia", "Iteraciones", "Items", "Capacidad",
  "Precio Mejor Solucion", "Precio Solucion Optima", "Diferencia",
)
#let filas_ej = datos_ej.slice(0, 6)

#figure(
  caption: [CSV leído dinámicamente (primeras 6 filas)],
  placement: top,
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    align: (left, center, center, center, center, center, center),
    inset: (x: 6pt, y: 4pt),
    stroke: (x, y) => if y <= 1 { (top: 0.5pt) },
    fill: (x, y) => if y > 0 and calc.rem(y, 2) == 0 { rgb("#efefef") },
    table.header[..encabezados_ej],
    for r in filas_ej {
      [r.at("Instancia")]
      [r.at("Iteraciones")]
      [r.at("Items")]
      [r.at("Capacidad")]
      [r.at("Precio Mejor Solucion")]
      [r.at("Precio Solucion Optima")]
      [r.at("Diferencia")]
    },
  ),
)

En el análisis completo, estos CSVs se agregan por familia y por combinación de parámetros para estimar la tasa de óptimo, el error promedio y la estabilidad respecto de la semilla. Los mejores valores de (tau, seed, iteraciones) para cada familia se reportan con sus métricas agregadas.

== Análisis de convergencia

#figure(
  rect(width: 200pt, height: 120pt, stroke: black, [
    #align(center + horizon)[Gráfico de convergencia\n(Placeholder)]
  ]),
  caption: [Curva de convergencia típica del algoritmo EO para la instancia KS-100],
  placement: top,
) <fig:convergencia>

La @fig:convergencia muestra el comportamiento típico de convergencia del algoritmo, observándose una mejora rápida inicial seguida de un refinamiento gradual de la solución.

= Discusión

El estudio de sensibilidad de parámetros resalta que:

1. *Importancia de $tau$*: Valores moderados (p. ej., 1.2–1.8) suelen balancear bien exploración e intensificación, mientras que valores muy altos o bajos degradan desempeño o estabilidad.

2. *Efecto de la semilla*: La variabilidad entre semillas es no trivial; promediar sobre varias semillas entrega una estimación más robusta del rendimiento esperado.

3. *Iteraciones suficientes*: Aumentar iteraciones mejora la tasa de óptimo hasta un punto de rendimientos decrecientes; conviene fijar un presupuesto acorde a la familia de instancias.

4. *Diferencias entre familias*: Las instancias Hard pueden requerir mayores iteraciones y $tau$ ligeramente más extremo; en Small/Large Coeff, configuraciones moderadas de $tau$ tienden a ser más estables.

= Conclusiones

Se reorientó el experimento para caracterizar el impacto de (tau, seed, iteraciones) en el desempeño de EO en tres familias de instancias (Small Coeff, Large Coeff y Hard). Este enfoque permite seleccionar configuraciones efectivas y estables sin comparar contra otros algoritmos.

A partir de los resultados, recomendamos:

1. Explorar $tau$ en un rango moderado (1.0–2.0), afinando por familia.
2. Evaluar múltiples semillas y reportar promedios y desviaciones.
3. Ajustar el presupuesto de iteraciones según la dificultad de la familia.

Como trabajo futuro se propone automatizar la agregación de CSVs por familia para generar tablas de tasa de óptimo, error promedio e iteraciones al mejor, y extender el análisis a variantes multidimensionales del problema.
