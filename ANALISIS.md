# Análisis

Nombre y código:

## Parte 1: cuatro herramientas, cuatro números

| Herramienta | Tiempo de `suma_primos(10000)` |
|---|---:|
| `time` | 6.584 ms |
| `timeit` (promedio de 20) | 3.200 ms |
| `cProfile` | 5.000 ms |
| `pyinstrument` | 6.000 ms |


### ¿Por qué no dan lo mismo?

1. **`time` (`perf_counter`)**: Mide el tiempo real transcurrido (wall-clock time) en una sola ejecución. Incluye el costo del arranque inicial, la carga en memoria y posibles interrupciones puntuales del sistema operativo (cambios de contexto o procesos en segundo plano).
2. **`timeit`**: Desactiva el recolector de basura (*garbage collector*) y ejecuta la función múltiples veces (20 ejecuciones), promediando el resultado. Esto elimina la varianza del primer arranque y las interferencias de la máquina, entregando el tiempo más "limpio" del algoritmo puro.
3. **`cProfile`**: Es un *profiler* determinista (por rastreo). Intercepta y contabiliza **cada llamada a función** (en este caso realizó más de 11,000 llamadas). Esa sobrecarga (*overhead*) constante ralentiza la ejecución del código.
4. **`pyinstrument`**: Es un *profiler* por muestreo (*statistical/sampling*). En lugar de rastrear cada llamada, interrumpe la ejecución a intervalos fijos (por defecto cada 1 ms) y registra la pila de llamadas (*stack trace*). Genera una sobrecarga mucho menor que `cProfile`, pero su precisión depende del intervalo de muestreo.

### ¿Cuál se acerca más al tiempo real y cuál lo deforma más?

* **El que más se acerca al tiempo real limpio:** **`timeit`**. Al promediar varias corridas y suspender el recolector de basura, minimiza las interferencias externas y ofrece la medición de rendimiento nativo más consistente de la función.
* **El que más lo deforma:** **`cProfile`**. Al registrar formalmente cada inicio y fin de función, impone una penalización de rendimiento por cada iteración. En algoritmos que realizan miles de llamadas a funciones pequeñas (como `es_primo`), el *overhead* de la herramienta distorsiona e infla sensiblemente el tiempo total frente a una ejecución normal.

## Parte 2: lo que mostró el perfil

Función que concentra el tiempo, cuántas veces se llama y cuánto suma
(copiar la línea de `cProfile`):

```text
  9998    0.004    0.000    0.004    0.000 src/suma_primos.py:3(es_primo)
## Parte 3: el producto punto tres veces

| Forma | Tiempo |
|---|---:|
| Indexando el arreglo de NumPy | 320.83 |
| Ciclo sobre listas | 149.41 |
| NumPy vectorizado | 5.45 |

¿Por qué indexar el arreglo de NumPy desde Python es la forma más lenta de
las tres? ¿Qué hace NumPy por debajo que el ciclo de Python no puede hacer?
¿Por qué indexar un arreglo de NumPy desde Python es la forma más lenta?Unboxing / Conversión de tipos en cada iteración:Un arreglo de NumPy guarda los datos de forma contigua en memoria como enteros puros de C (sin metadatos de Python). Cuando haces a[i] dentro de un ciclo de Python, NumPy debe tomar ese entero de C, instanciar un nuevo objeto PyObject en memoria para Python y pasárselo al intérprete. Crear y destruir millones de objetos de Python dentro del bucle destruye el rendimiento. En cambio, una lista nativa de Python ya tiene las referencias a los objetos PyObject listos para usarse.Carga del motor de Python (Interpreted Loop Overhead):El ciclo for en Python evalúa en cada paso el tipo de variable, revisa límites, realiza llamadas a funciones de extracción e interpreta el bytecode línea por línea.¿Qué hace NumPy por debajo que el ciclo de Python no puede hacer?Cálculo en C / Fortran compilado:NumPy ejecuta las operaciones mediante código compilado directamente en C. Todo el bucle ocurre dentro de C sin tocar el máquina de estado ni el intérprete de Python hasta que termina.Memoria contigua y Caché del CPU:Los elementos de un arreglo de NumPy están ordenados consecutivamente en memoria. Esto permite al procesador aprovechar la caché L1/L2/L3 mediante prefetching (leer bloques contiguos de memoria antes de que se necesiten). Las listas de Python son listas de punteros dispersos por la memoria RAM, provocando cache misses.Vectorización e Instrucciones SIMD:Las CPU modernas tienen instrucciones SIMD (Single Instruction, Multiple Data como AVX-512 o ARM Neon). NumPy utiliza librerías de álgebra lineal optimizadas (como BLAS/LAPACK) que pueden multiplicar y sumar varios números (por ejemplo, 4 u 8 enteros de 64 bits) en un solo ciclo de reloj de la CPU.

## Parte 4: AVX a mano

| Versión | Tiempo | Resultado |
|---|---:|---:|
| Escalar |  |  |
| AVX |  |  |

Factor obtenido, y por qué no llega a ocho aunque cada instrucción opere
ocho floats:
