"""Pendiente: medir suma_primos(10000) e imprimir el tiempo en milisegundos."""
from profile import Profile
import sys
from pathlib import Path
from pyinstrument import Profiler

# Sube dos niveles desde 'scripts' para llegar a la raíz del proyecto
# (scripts -> infra-profiling-en-python)
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# Ahora Python sabrá encontrar la carpeta 'src'
from src.suma_primos import suma_primos

with Profiler(interval=0.001) as profiler:
    resultado = suma_primos(10000) 
    
print(profiler.output_text(unicode=True, color=True))
with open("pyinstrument_results.html", "w") as f:
    f.write(profiler.output_html())
