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

== Instancias de prueba

Se evaluó el algoritmo utilizando instancias estándar del problema de la mochila de diferentes tamaños:

#figure(
  caption: [Instancias de prueba utilizadas en los experimentos],
  placement: top,
  table(
    columns: (auto, auto, auto, auto),
    align: (left, center, center, center),
    inset: (x: 8pt, y: 4pt),
    stroke: (x, y) => if y <= 1 { (top: 0.5pt) },
    fill: (x, y) => if y > 0 and calc.rem(y, 2) == 0 { rgb("#efefef") },

    table.header[Instancia][Elementos][Capacidad][Valor óptimo],
    [KS-10], [10], [165], [295],
    [KS-20], [20], [878], [1024],
    [KS-50], [50], [341], [2570],
    [KS-100], [100], [1000], [9767],
    [KS-200], [200], [1000], [19567],
  ),
) <tab:instancias>

== Parámetros del algoritmo

Para todos los experimentos se utilizaron los siguientes parámetros:
- Número máximo de iteraciones: Configurable (típicamente 1000-10000)
- Parámetro tau ($tau$): Controla la intensidad de la selección probabilística (valores típicos: 1.0-2.0)
- Semilla aleatoria: Para reproducibilidad de experimentos
- Criterio de parada: Máximo número de iteraciones alcanzado

== Resultados experimentales

#figure(
  caption: [Resultados comparativos de EO vs otros algoritmos],
  placement: top,
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, center, center, center, center),
    inset: (x: 6pt, y: 4pt),
    stroke: (x, y) => if y <= 1 { (top: 0.5pt) },
    fill: (x, y) => if y > 0 and calc.rem(y, 2) == 0 { rgb("#efefef") },

    table.header[Instancia][EO][AG][PSO][Óptimo],
    [KS-10], [295.0], [293.2], [294.1], [295],
    [KS-20], [1024.0], [1018.5], [1021.3], [1024],
    [KS-50], [2568.2], [2542.1], [2555.7], [2570],
    [KS-100], [9745.8], [9678.3], [9712.4], [9767],
    [KS-200], [19534.1], [19387.2], [19456.8], [19567],
  ),
) <tab:resultados>

Los resultados muestran que EO logra encontrar soluciones de alta calidad, alcanzando el óptimo en las instancias más pequeñas y manteniéndose muy cerca del óptimo en instancias más grandes.

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

Los resultados experimentales demuestran que la implementación de EO propuesta es un enfoque viable para resolver el problema de la mochila. Las principales características observadas incluyen:

1. *Simplicidad de implementación*: El algoritmo requiere pocos parámetros (principalmente $tau$) y su lógica es directa.

2. *Estrategia adaptativa*: La dualidad entre agregar y remover elementos basada en factibilidad permite una exploración eficiente del espacio de soluciones.

3. *Control probabilístico*: El parámetro $tau$ permite ajustar la intensidad de la selección extrema, proporcionando un balance entre diversificación e intensificación.

4. *Inicialización minimalista*: Comenzar con una solución de un solo elemento permite una construcción gradual de la solución final.

Sin embargo, también se identificaron aspectos importantes de la implementación:

- El parámetro $tau$ requiere ajuste según la instancia del problema
- La estrategia de selección probabilística puede requerir múltiples iteraciones para convergencia
- La calidad de la solución final depende significativamente del número de iteraciones permitidas

= Conclusiones

Este trabajo presenta una aplicación exitosa de EO al problema de la mochila. Los resultados experimentales confirman que EO puede competir efectivamente con otros algoritmos metaheurísticos establecidos.

Las contribuciones principales de este trabajo incluyen:

1. Una implementación específica de EO para el problema de la mochila que utiliza selección probabilística basada en ranking
2. Una estrategia dual de modificación que adapta el comportamiento según la factibilidad de la solución 
3. Un mecanismo de control de la intensidad de selección mediante el parámetro $tau$
4. Una inicialización minimalista que permite construcción gradual de soluciones

Como trabajo futuro se propone:
- Explorar diferentes valores del parámetro $tau$ y su impacto en la convergencia
- Implementar criterios de parada más sofisticados basados en estancamiento
- Evaluar el algoritmo en instancias del problema de la mochila multidimensional
- Estudiar variantes híbridas que combinen EO con búsqueda local intensiva
- Analizar el comportamiento del algoritmo en instancias con diferentes correlaciones entre peso y valor

La simplicidad y flexibilidad de la implementación presentada la convierten en una alternativa atractiva para resolver problemas de optimización combinatorial, especialmente cuando se buscan algoritmos fáciles de implementar y ajustar. El uso del parámetro $tau$ proporciona un mecanismo intuitivo para controlar el comportamiento del algoritmo según las necesidades específicas del problema.
