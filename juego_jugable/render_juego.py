# -*- coding: utf-8 -*-
"""
Todo lo que depende de pygame.draw / pygame.font para pintar la partida en curso:
el pato, el splash de sangre y el HUD (contador de disparos + barra de tiempo).

La conversión NumPy -> pygame.Surface para sprites con transparencia (RGBA) usa
pygame.image.frombuffer(), NO pygame.surfarray.make_surface() como en tablero.py.
La diferencia importa y vale la pena explicarla:
  - make_surface() espera un arreglo indexado [x, y, canal] (por eso ahí sí
    transponemos), y no soporta un 4to canal alfa directamente.
  - frombuffer() lee los bytes tal cual como estén en memoria (fila por fila,
    igual que NumPy los guarda) y sí entiende un formato "RGBA" con transparencia,
    así que para sprites con alfa es la ruta más directa -- no hace falta transponer.
"""
import numpy as np
import pygame

from constantes import AMARILLO, GRIS_OSCURO, ROJO, VERDE_NES


def numpy_rgba_a_superficie(imagen_rgba):
    imagen_rgba = np.ascontiguousarray(imagen_rgba, dtype=np.uint8)
    alto, ancho = imagen_rgba.shape[0], imagen_rgba.shape[1]
    superficie = pygame.image.frombuffer(imagen_rgba.tobytes(), (ancho, alto), "RGBA")
    return superficie.convert_alpha()


def dibujar_pato(pantalla, tablero, ronda, sprite_pato):
    if ronda.estado != ronda.ESPERANDO_CLIC:
        return
    fila, columna = ronda.posicion_pato
    x, y = tablero.centro_celda_pantalla(fila, columna)
    rect = sprite_pato.get_rect(center=(x, y))
    pantalla.blit(sprite_pato, rect)


def dibujar_resultado_ronda(pantalla, tablero, ronda, sprite_splash):
    """Splash rojo si fue acierto; una X gris si fue fallo (se ve un instante tras resolver la ronda)."""
    if ronda.estado != ronda.RESUELTA:
        return
    fila, columna = ronda.posicion_pato
    x, y = tablero.centro_celda_pantalla(fila, columna)

    if ronda.acierto:
        rect = sprite_splash.get_rect(center=(x, y))
        pantalla.blit(sprite_splash, rect)
    else:
        tam = tablero.tam_celda_pantalla() // 3
        pygame.draw.line(pantalla, GRIS_OSCURO, (x - tam, y - tam), (x + tam, y + tam), width=4)
        pygame.draw.line(pantalla, GRIS_OSCURO, (x - tam, y + tam), (x + tam, y - tam), width=4)


def dibujar_hud(pantalla, fuente, ronda, numero_ronda, total_disparos, aciertos):
    texto = fuente.render(
        f"Disparo {numero_ronda}/{total_disparos}   Aciertos: {aciertos}", True, VERDE_NES
    )
    pantalla.blit(texto, (20, 10))

    # Barra de tiempo restante para reaccionar
    ancho_barra = 300
    alto_barra = 14
    x_barra, y_barra = pantalla.get_width() - ancho_barra - 20, 14
    proporcion = ronda.tiempo_restante() / ronda.tiempo_limite if ronda.tiempo_limite else 0
    color_barra = VERDE_NES if proporcion > 0.35 else ROJO

    pygame.draw.rect(pantalla, GRIS_OSCURO, (x_barra, y_barra, ancho_barra, alto_barra))
    pygame.draw.rect(pantalla, color_barra, (x_barra, y_barra, int(ancho_barra * proporcion), alto_barra))
    pygame.draw.rect(pantalla, VERDE_NES, (x_barra, y_barra, ancho_barra, alto_barra), width=1)
