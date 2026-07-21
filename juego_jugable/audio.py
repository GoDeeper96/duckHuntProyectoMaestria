# -*- coding: utf-8 -*-
"""
Sonido sintetizado con NumPy, reproducido con pygame.mixer.

Es la MISMA fórmula que generar_tono() en el notebook (onda senoidal + envolvente
fade-in/fade-out) -- lo único que cambia es el mecanismo de reproducción:
  - Notebook (Jupyter): IPython.display.Audio, pensado para reproducir un array
    dentro de la celda de salida.
  - Acá (pygame): pygame.sndarray.make_sound(), que necesita el array como
    enteros de 16 bits (int16), no floats en [-0.5, 0.5] como genera generar_tono().
    Por eso _onda_a_sonido() hace ese escalado antes de crear el Sound.
"""
import numpy as np
import pygame

import logica
from constantes import TASA_MUESTREO_AUDIO

_audio_disponible = False


def inicializar_audio():
    """Intenta inicializar el mezclador de audio. Si no hay dispositivo de sonido
    disponible (por ejemplo, corriendo en un entorno sin salida de audio), el juego
    sigue funcionando en silencio en vez de detenerse con un error."""
    global _audio_disponible
    try:
        pygame.mixer.init(frequency=TASA_MUESTREO_AUDIO, size=-16, channels=1)
        _audio_disponible = True
    except pygame.error:
        _audio_disponible = False
        print("Aviso: no se pudo inicializar el audio; el juego seguirá sin sonido.")


def _onda_a_sonido(onda):
    onda_int16 = np.clip(onda * 32767, -32768, 32767).astype(np.int16)

    # Aunque pedimos channels=1 al inicializar, algunos sistemas (o el driver "dummy"
    # usado en pruebas sin salida de audio) igual arrancan el mezclador en estéreo.
    # pygame.mixer.get_init() dice lo que realmente quedó activo; si es estéreo, el
    # array debe ser 2D (una columna por canal), si no pygame.sndarray lo rechaza.
    info_mezclador = pygame.mixer.get_init()
    canales = info_mezclador[2] if info_mezclador else 1
    if canales == 2:
        onda_int16 = np.column_stack([onda_int16, onda_int16])

    return pygame.sndarray.make_sound(onda_int16)


def sonido_acierto():
    """Dos tonos agudos ascendentes (880 Hz -> 1320 Hz)."""
    if not _audio_disponible:
        return
    onda = np.concatenate([
        logica.generar_tono(880, 0.12, tasa_muestreo=TASA_MUESTREO_AUDIO),
        logica.generar_tono(1320, 0.18, tasa_muestreo=TASA_MUESTREO_AUDIO),
    ])
    _onda_a_sonido(onda).play()


def sonido_fallo():
    """Un tono grave y prolongado (150 Hz)."""
    if not _audio_disponible:
        return
    onda = logica.generar_tono(150, 0.4, tasa_muestreo=TASA_MUESTREO_AUDIO)
    _onda_a_sonido(onda).play()
