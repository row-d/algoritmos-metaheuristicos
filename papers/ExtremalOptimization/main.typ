#set text(lang: "es")
#import "@preview/charged-ieee:0.1.4": ieee
#import "@preview/lovelace:0.3.0": *
#import "@preview/cetz:0.4.2"
#import "@preview/cetz-plot:0.1.3": plot, chart



#show: ieee.with(
  title: [Optimización Extrema aplicada al problema de la mochila],
  abstract: [
    Este artículo presenta la aplicación del algoritmo de Optimización Extrema (EO, del inglés Extreme Optimization) para resolver el problema clásico de la mochila. EO es una metaheurística inspirada en el concepto de criticalidad auto-organizada, que se caracteriza por realizar modificaciones probabilísticas extremas en las soluciones. Se implementa una variante que utiliza selección por rango con parámetro de temperatura ($tau$) y una estrategia dual que adapta el comportamiento según la factibilidad de la solución actual. La implementación emplea una inicialización minimalista y un mecanismo de selección probabilística que balancea exploración e intensificación, demostrando ser un enfoque simple pero efectivo para el problema de la mochila.
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

El problema de la mochila@kellerer2004 es uno de los problemas de optimización combinatoria más estudiados en la literatura científica. Formalmente, consiste en seleccionar un subconjunto de elementos de un conjunto dado, cada uno con un peso y un valor asociado, de manera que se maximice el valor total sin exceder la capacidad de peso de la mochila @dantzig1957.


Este problema pertenece a la clase NP-hard, lo que significa que no existe un algoritmo de tiempo polinomial que garantice encontrar la solución óptima para todas las instancias. Por esta razón, los algoritmos metaheurísticos han ganado popularidad como enfoques efectivos para resolver instancias grandes del problema en tiempo razonable.


Los algoritmos genéticos han sido ampliamente estudiados para variantes de la mochila, como se muestra en @khuri1994 y en el texto clásico de Goldberg @goldberg1989. Por otra parte, la Optimización Extrema (EO) ha sido aplicada exitosamente a distintos problemas combinatorios, incluyendo implementaciones generales @randall2005 y aplicaciones específicas a mochilas multidimensionales @chen2007.


La EO es una metaheurística relativamente nueva propuesta por Boettcher y Percus en 1999 @boettcher1999. Se inspira en el concepto de criticalidad auto-organizada @bak1987 observado en sistemas complejos de la física, donde pequeñas perturbaciones locales pueden llevar a cambios dramáticos en el sistema completo.

== Características de EO

EO se diferencia de otros algoritmos evolutivos en varios aspectos fundamentales:

1. *Operación sobre un solo individuo*: A diferencia de los algoritmos genéticos que mantienen una población, EO trabaja con una sola solución que evoluciona iterativamente.

2. *Selección extrema*: En cada iteración, se identifica el componente "más malo" de la solución actual y se modifica de manera aleatoria.

3. *No utiliza información de aptitud global*: La decisión de qué modificar se basa únicamente en la evaluación local de cada componente.

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

=== Función de aptitud y selección

La implementación utiliza la relación valor/peso ($v_i / w_i$) como medida de calidad para cada elemento. El algoritmo emplea un mecanismo de selección por ruleta sesgada con un parámetro $tau$ que controla la intensidad de la selección:

$
  p_k = k^{-tau}
$ <eq:prob-seleccion>

donde $k$ es el rango del elemento cuando se ordena por su valor de aptitud, y $tau$ es el parámetro de temperatura que controla qué tan extrema es la selección. Valores altos de $tau$ favorecen la selección de elementos con peor aptitud (más extrema), mientras que valores bajos hacen la selección más uniforme.

=== El parámetro tau y su impacto

El parámetro $tau$ es fundamental en la implementación y controla el balance entre diversificación e intensificación:

- *$tau$ alto (ej. $tau = 2.0$)*: Selección muy extrema, favorece fuertemente elementos con peor aptitud. Promueve exploración agresiva.
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
    + Calcular aptitud $f_i = v_i / w_i$ para cada elemento $i$
    + $x_"mejor" arrow.l x$ // Guardar mejor solución encontrada
    + *repetir* hasta criterio de parada:
      + *si* solución actual es factible *entonces*
        + // Intentar agregar un elemento (mejorar solución)
        + Obtener elementos no incluidos ($x_i = 0$)
        + Ordenar por aptitud descendente
        + Generar vector de probabilidades: $p_k = k^{-tau}$
        + Seleccionar elemento mediante ruleta e incluirlo
      + *sino*
        + // Remover elemento para mantener factibilidad  
        + Obtener elementos incluidos ($x_i = 1$)
        + Ordenar por aptitud ascendente
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

El análisis experimental se enfoca exclusivamente en estudiar la sensibilidad del algoritmo EO a tres parámetros: $tau$, la semilla aleatoria y el número máximo de iteraciones. Para ello, se utilizan tres familias de instancias ampliamente empleadas en la literatura @pisinger2005:



== Diseño experimental y parámetros

El objetivo es identificar configuraciones de (tau, seed, iteraciones) que ofrecen el mejor desempeño por familia de instancias. Para cada conjunto se evalúan combinaciones de parámetros siguiendo una rejilla configurable.

- Parámetro $tau$: controla la intensidad de la selección probabilística ($p_k = k^{-tau}$). Valores de referencia: 0.8–2.0.
- Semilla (seed): controla la reproducibilidad. Se exploran múltiples semillas para medir variabilidad.
- Iteraciones: máximo de pasos de EO. Valores de referencia: 500–10000.

Métricas reportadas por instancia y luego agregadas por familia:

- Tasa de óptimo: proporción de instancias con diferencia 0.
- Ratio Promedio: Medida de calidad definida como el cociente entre el mejor valor encontrado y el óptimo conocido ($v_"best" / v_"opt"$). Un valor de 1.0 indica que se alcanzó el óptimo.
- Error absoluto promedio: promedio de precio_mejor - precio_óptimo.
- Iteraciones hasta el mejor: número de iteraciones consumidas al lograr la mejor solución.

== Ejecución y recolección de resultados

La recolección de datos se realizó ejecutando el algoritmo sobre los tres conjuntos de instancias (Small, Large y Hard) variando los parámetros de interés. Los resultados crudos, que incluyen el mejor valor encontrado, el óptimo conocido y las iteraciones utilizadas, se almacenaron en archivos CSV para su posterior procesamiento.

En el análisis posterior, estos resultados se agregaron por familia y por combinación de parámetros para estimar la tasa de óptimo, el error promedio y la estabilidad respecto de la semilla. Los mejores valores de (tau, seed, iteraciones) para cada familia se reportan con sus métricas agregadas.

== Análisis de convergencia y desempeño

A continuación se presentan los gráficos de evolución del ratio promedio (calidad) respecto a las iteraciones reales promedio consumidas, para diferentes valores de $tau$.

#let plot_ratio_iter(data_path, title_text, x_step: 1000, show_marks: false) = {
  let raw_data = csv(data_path)
  // Skip header
  let data = raw_data.slice(1)
  // Columns: tau(0), max_iterations(1), mean_ratio(2), std_ratio(3), mean_gap(4), mean_iterations_used(5), ...
  
  // Filter unique taus for legend
  let taus = ()
  for row in data {
    let t = row.at(0)
    if not taus.contains(t) { taus.push(t) }
  }
  taus = taus.sorted()

  figure(
    cetz.canvas({
      plot.plot(
        size: (5, 3.5),
        x-tick-step: x_step,
        x-label: "Iteraciones Promedio",
        y-label: "Ratio Promedio (Mejor/Óptimo)",
        title: title_text,
        legend: "inner-south-east",
        y-min: 0.99, y-max: 1.0005, // Zoom to high quality area
        {
          let colors = (red, blue, green, orange, purple, black)
          for (i, t) in taus.enumerate() {
             let series = data.filter(r => r.at(0) == t).map(r => (float(r.at(5)), float(r.at(2))))
             // Sort by iterations to draw line correctly
             series = series.sorted(key: x => x.at(0))
             plot.add(series, label: "tau=" + t, mark: if show_marks {"o"} else {none}, mark-size: 0.05, style: (stroke: colors.at(calc.rem(i, colors.len()))))
          }
        }
      )
    }),
    caption: [Evolución de calidad vs costo real para ] + title_text
  )
}

#plot_ratio_iter("agg_small.csv", "Instancias Small")
#plot_ratio_iter("agg_large.csv", "Instancias Large")
#plot_ratio_iter("agg_hard.csv", "Instancias Hard", x_step: 50, show_marks: true)



== Análisis de variabilidad

Para complementar el análisis de promedios, se presenta la distribución de la calidad de las soluciones (Ratio) para diferentes valores de $tau$, utilizando diagramas de caja simplificados (min, Q1, mediana, Q3, max). Esto permite visualizar la estabilidad del algoritmo.

#let boxplot_graph(data_path, title_text) = {
  let raw_data = csv(data_path)
  let data = raw_data.slice(1)
  // Columns: tau(0), min(1), q1(2), median(3), q3(4), max(5)

  figure(
    cetz.canvas({
      plot.plot(
        size: (5, 3.5),
        x-label: "Tau",
        y-label: "Ratio (Calidad)",
        title: title_text,
        y-min: 0.0, y-max: 1.05,
        {
           let formatted_data = data.map(row => (
             x: float(row.at(0)), 
             min: float(row.at(1)), 
             q1: float(row.at(2)), 
             q2: float(row.at(3)), 
             q3: float(row.at(4)), 
             max: float(row.at(5))
           ))
           plot.add-boxwhisker(formatted_data, box-width: 0.15)
        }
      )
    }),
    caption: [Distribución de calidad vs Tau para ] + title_text
  )
}

#boxplot_graph("box_small.csv", "Instancias Small (1000 iter)")
#boxplot_graph("box_large.csv", "Instancias Large (1000 iter)")
#boxplot_graph("box_hard.csv", "Instancias Hard (500 iter)")

= Discusión

El estudio de sensibilidad de parámetros resalta que:

1. *Importancia de $tau$*: Valores moderados (p. ej., 1.2–1.8) suelen balancear bien exploración e intensificación, mientras que valores muy altos o bajos degradan desempeño o estabilidad.

2. *Efecto de la semilla*: La variabilidad entre semillas es no trivial; promediar sobre varias semillas entrega una estimación más robusta del rendimiento esperado.

3. *Iteraciones suficientes*: Aumentar iteraciones mejora la tasa de óptimo hasta un punto de rendimientos decrecientes; conviene fijar un presupuesto acorde a la familia de instancias.

4. *Diferencias entre familias*: Las instancias Hard pueden requerir mayores iteraciones y $tau$ ligeramente más extremo; en Small/Large Coeff, configuraciones moderadas de $tau$ tienden a ser más estables.

= Conclusiones

Se reorientó el experimento para caracterizar el impacto de (tau, seed, iteraciones) en el desempeño de EO en tres familias de instancias (Small Coeff, Large Coeff y Hard). Este enfoque permite seleccionar configuraciones efectivas y estables sin comparar contra otros algoritmos.

A partir de los resultados y el análisis de iteraciones, se concluye:

- *Small*: Al analizar las iteraciones, se observa que configuraciones con $tau$ alto (1.8-2.0) logran ratios $>99.9%$ convergiendo a menudo antes del límite de iteraciones. La recomendación eficiente apunta a $tau=1.8$ con un límite de 1000 iteraciones, donde el promedio de iteraciones es bajo pero la calidad es muy alta.
- *Large*: Similarmente, $tau=1.6$ muestra un excelente balance. Aunque se configure un `max_iterations` alto (e.g. 5000), el análisis de iteraciones muestra el costo verdadero. Para eficiencia, $tau=1.6$ con `max_iterations=1000` es suficiente para estar en el rango del 99.5% del óptimo.
- *Hard*: El costo en iteraciones es muy bajo ($approx 118$) e independiente del `max_iterations` configurado, ya que el algoritmo encuentra el óptimo rápidamente. $tau=1.8$ minimiza consistentemente este número de iteraciones.

== Recomendaciones Sintéticas

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, center, center, center, left),
    inset: 5pt,
    table.header([*Tipo*], [*tau*], [*max_iter (param)*], [*Iteraciones*], [*Justificación*]),
    [Small], [1.8], [1000], [~1000], [Alta eficiencia y calidad],
    [Large], [1.6], [1000], [~1000], [Buen balance costo/calidad],
    [Hard],  [1.8], [500],  [~118],  [Convergencia más rápida al óptimo],
  ),
  caption: [Recomendación de parámetros basada en eficiencia]
)

El uso de *iteraciones* como métrica de costo confirma que no es necesario sobre-dimensionar `max_iterations` para obtener resultados de alta calidad en estos conjuntos de datos.

Como trabajo futuro se propone extender el análisis a variantes multidimensionales del problema y evaluar el impacto del tiempo de cómputo (tiempo real de ejecución).
