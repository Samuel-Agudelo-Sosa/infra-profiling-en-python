import sys
from pathlib import Path
import time

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.suma_primos import suma_primos

inicio = time.perf_counter()
suma_primos(10000)
fin = time.perf_counter()

tiempo_ms = (fin - inicio) * 1000
print(f"{tiempo_ms:.3f} ms")