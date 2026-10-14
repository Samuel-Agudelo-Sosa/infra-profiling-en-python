import sys
from pathlib import Path
from cProfile import Profile
from pstats import Stats

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.suma_primos import suma_primos

with Profile() as profiler:
    suma_primos(10000)

stats = Stats(profiler)
tiempo_ms = stats.total_tt * 1000
print(f"{tiempo_ms:.3f} ms")