import sys
from pathlib import Path
from timeit import timeit

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.suma_primos import suma_primos

iterations = 20
total_time = timeit(
    "suma_primos(10000)", 
    number=iterations,
    globals=globals()
)

# timeit da segundos; convertimos a ms y promediamos
promedio_ms = (total_time / iterations) * 1000
print(f"{promedio_ms:.3f} ms")