import sys
from pathlib import Path
import time
from pyinstrument import Profiler

# Resolver ruta raíz
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.suma_primos import suma_primos

profiler = Profiler()

# Medimos el tiempo que toma el bloque con pyinstrument
inicio = time.perf_counter()
profiler.start()
suma_primos(10000)
profiler.stop()
fin = time.perf_counter()

# Guardar el reporte HTML obligatorio
with open("pyinstrument_results.html", "w") as f:
    f.write(profiler.output_html())

# Imprimir ÚNICAMENTE el tiempo en ms
tiempo_ms = (fin - inicio) * 1000
print(f"{tiempo_ms:.3f} ms")