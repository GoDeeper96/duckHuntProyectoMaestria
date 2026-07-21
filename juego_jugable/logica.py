# -*- coding: utf-8 -*-
"""
Lógica pura del juego: matrices, conversión de imágenes, aleatoriedad y estadísticas.

Nada en este archivo depende de pygame ni de tkinter — son las mismas fórmulas que
en `DuckHunt_Simulacion.ipynb` (Secciones 3, 4, 6, 8 y 9), reimplementadas aquí porque
un notebook no se puede importar como módulo de Python. Mantenerlas separadas de la
capa de dibujo (`render.py`) es lo que nos permite explicar y probar cada fórmula
de forma aislada, sin necesitar una ventana abierta.
"""
import numpy as np
import pandas as pd
from PIL import Image

# ============================================================
# IMÁGENES: escala de grises, blanco/negro, chroma-key
# ============================================================
PESOS_LUMINOSIDAD = np.array([0.299, 0.587, 0.114])  # pesos R, G, B
UMBRAL_BN = 128


def cargar_fondo(ruta):
    """Carga una imagen y la devuelve como matriz NumPy RGB, componiendo el alfa sobre blanco si tiene."""
    imagen = Image.open(ruta)
    if imagen.mode == "RGBA":
        fondo_blanco = Image.new("RGB", imagen.size, (255, 255, 255))
        fondo_blanco.paste(imagen, mask=imagen.split()[3])
        imagen = fondo_blanco
    else:
        imagen = imagen.convert("RGB")
    return np.array(imagen)


def convertir_a_grises(imagen_rgb):
    """Fórmula de luminosidad: 0.299 R + 0.587 G + 0.114 B (igual que en el notebook)."""
    return np.dot(imagen_rgb[..., :3], PESOS_LUMINOSIDAD).astype(np.uint8)


def convertir_a_bn(imagen_grises, umbral=UMBRAL_BN):
    """Binariza: píxeles >= umbral -> blanco (255), el resto -> negro (0)."""
    return np.where(imagen_grises >= umbral, 255, 0).astype(np.uint8)


def quitar_fondo_solido(imagen_rgba, tolerancia=40):
    """Chroma-key: vuelve transparente todo píxel a distancia <= tolerancia del color de la esquina."""
    imagen = imagen_rgba.copy()
    color_fondo = imagen[0, 0, :3].astype(float)
    distancia = np.sqrt(np.sum((imagen[..., :3].astype(float) - color_fondo) ** 2, axis=-1))
    imagen[..., 3] = np.where(distancia <= tolerancia, 0, imagen[..., 3])
    return imagen


def cargar_sprite_sin_fondo(ruta, tam_px, tolerancia_fondo=40):
    """Carga un sprite, le quita el fondo sólido y lo redimensiona a tam_px x tam_px."""
    imagen = Image.open(ruta).convert("RGBA")
    arreglo = quitar_fondo_solido(np.array(imagen), tolerancia_fondo)
    imagen_redimensionada = Image.fromarray(arreglo).resize((tam_px, tam_px), Image.LANCZOS)
    return np.array(imagen_redimensionada)


# ============================================================
# GRID: bordes de celdas y conversión pixel <-> celda
# ============================================================
def construir_bordes_grid(alto, ancho, filas, columnas):
    """Bordes en píxeles de cada celda -- ver explicación con ejemplo en la Sección 3 del notebook."""
    bordes_fila = np.linspace(0, alto, filas + 1, dtype=int)
    bordes_columna = np.linspace(0, ancho, columnas + 1, dtype=int)
    return bordes_fila, bordes_columna


def centro_celda(i, j, bordes_fila, bordes_columna):
    """Coordenadas (x, y) en píxeles del centro de la celda (i, j)."""
    y = (bordes_fila[i] + bordes_fila[i + 1]) // 2
    x = (bordes_columna[j] + bordes_columna[j + 1]) // 2
    return x, y


def celda_en_pixel(x, y, bordes_fila, bordes_columna):
    """
    Convierte un punto (x, y) en píxeles -- por ejemplo, la posición de un clic del mouse --
    a un índice de celda (fila, columna). Es la operación inversa a centro_celda(), y es la
    base de la colisión "por celda" que usa el modo jugable: en vez de comparar rectángulos
    o píxeles exactos, reducimos el clic a la misma unidad atómica que ya usa toda la
    simulación (una celda de la cuadrícula), y comparamos índices.

    Devuelve None si (x, y) cae fuera del tablero.
    """
    fila = np.searchsorted(bordes_fila, y, side="right") - 1
    columna = np.searchsorted(bordes_columna, x, side="right") - 1

    filas_totales = len(bordes_fila) - 1
    columnas_totales = len(bordes_columna) - 1
    if not (0 <= fila < filas_totales) or not (0 <= columna < columnas_totales):
        return None
    return int(fila), int(columna)


# ============================================================
# ALEATORIEDAD
# ============================================================
def generar_posicion_aleatoria(filas, columnas):
    """Elige una celda (fila, columna) al azar dentro del grid, usando NumPy."""
    return int(np.random.randint(0, filas)), int(np.random.randint(0, columnas))


def generar_mascara_splash(tam_px, n_manchas=6, color=(200, 0, 0)):
    """Textura RGBA con manchas circulares rojas en posiciones/radios aleatorios (splash de impacto)."""
    splash = np.zeros((tam_px, tam_px, 4), dtype=np.uint8)
    filas_px, columnas_px = np.mgrid[0:tam_px, 0:tam_px]
    centros_x = np.random.randint(0, tam_px, n_manchas)
    centros_y = np.random.randint(0, tam_px, n_manchas)
    radios = np.random.randint(tam_px // 10, tam_px // 4, n_manchas)
    for cx, cy, radio in zip(centros_x, centros_y, radios):
        distancia = np.sqrt((columnas_px - cx) ** 2 + (filas_px - cy) ** 2)
        mascara = distancia <= radio
        splash[mascara, 0] = color[0]
        splash[mascara, 1] = color[1]
        splash[mascara, 2] = color[2]
        splash[mascara, 3] = 180
    return splash


# ============================================================
# AUDIO: síntesis de tonos (misma fórmula que el notebook)
# ============================================================
def generar_tono(frecuencia, duracion=0.3, amplitud=0.5, tasa_muestreo=44100):
    """Onda senoidal y(t) = A*sin(2*pi*f*t) con envolvente fade-in/fade-out."""
    t = np.linspace(0, duracion, int(tasa_muestreo * duracion), endpoint=False)
    onda = amplitud * np.sin(2 * np.pi * frecuencia * t)
    n_fade = max(1, int(0.1 * len(t)))
    envolvente = np.ones_like(onda)
    envolvente[:n_fade] = np.linspace(0, 1, n_fade)
    envolvente[-n_fade:] = np.linspace(1, 0, n_fade)
    return onda * envolvente


# ============================================================
# VALIDACIÓN Y ESTADÍSTICAS
# ============================================================
def validar_impacto(posicion_pato, posicion_disparo):
    """Compara dos posiciones (fila, columna). True si coinciden (acierto)."""
    return posicion_pato is not None and posicion_pato == posicion_disparo


def calcular_estadisticas(registros, nombre_jugador, tam_grid):
    """A partir de la lista de registros (uno por disparo), arma el resumen de la partida."""
    df = pd.DataFrame(registros)
    total = len(df)
    exitosos = int(df["acierto"].sum()) if total else 0
    errados = total - exitosos
    return {
        "jugador": nombre_jugador,
        "grid": f"{tam_grid}x{tam_grid}",
        "total_disparos": total,
        "disparos_exitosos": exitosos,
        "disparos_errados": errados,
        "porcentaje_aciertos": round(100 * exitosos / total, 1) if total else 0.0,
        "porcentaje_fallos": round(100 * errados / total, 1) if total else 0.0,
    }
