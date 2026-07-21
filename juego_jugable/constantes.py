# -*- coding: utf-8 -*-
"""
Constantes compartidas del modo jugable: rutas, colores, límites de configuración.

Se separan en su propio módulo (en vez de repetirlas en cada archivo) para que
cualquier ajuste (un color, un límite, una ruta) se cambie en un solo lugar.
"""
from pathlib import Path

# ============================================================
# RUTAS
# ============================================================
# Este archivo vive en FinalProjectP101/juego_jugable/, los assets están un nivel arriba.
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_ASSETS = RAIZ_PROYECTO / "assets"
RUTA_FONDO = RUTA_ASSETS / "paisaje-limpio (2).png"
RUTA_PATO = RUTA_ASSETS / "pato (1).png"
RUTA_GANADOR = RUTA_ASSETS / "ganador.jpeg"
RUTA_GAMEOVER = RUTA_ASSETS / "gameover.jpg"

# CSV separado del que usa el notebook: miden habilidades distintas (reacción/puntería
# vs. una simulación puramente aleatoria) y mezclarlos en las mismas estadísticas
# daría una comparación engañosa entre jugadores.
RUTA_CSV_REGISTROS = RAIZ_PROYECTO / "juego_jugable" / "registros_jugadores_interactivo.csv"

# ============================================================
# VENTANA
# ============================================================
ANCHO_VENTANA = 960
ALTO_VENTANA = 620
FPS = 60

# ============================================================
# COLORES (RGB) — paleta estilo consola retro (fondo negro, texto verde fósforo)
# ============================================================
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE_NES = (57, 255, 20)
AMARILLO = (255, 221, 0)
ROJO = (220, 40, 40)
GRIS_OSCURO = (40, 40, 40)

# ============================================================
# LÍMITES DE CONFIGURACIÓN (pantalla NES)
# ============================================================
GRID_MIN, GRID_MAX = 3, 8
DISPAROS_MIN, DISPAROS_MAX = 5, 99
NOMBRE_MAX_LEN = 10
ALFABETO_NES = ["_"] + [chr(c) for c in range(ord("A"), ord("Z") + 1)]

# ============================================================
# REGLAS DEL MODO JUGABLE
# ============================================================
TIEMPO_LIMITE_PATO = 1.5  # segundos que el pato permanece visible antes de "escapar"
TASA_MUESTREO_AUDIO = 44100
