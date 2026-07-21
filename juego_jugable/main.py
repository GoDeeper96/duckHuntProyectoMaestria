# -*- coding: utf-8 -*-
"""
Punto de entrada del modo jugable.

Estados del juego (máquina de estados simple, un string en `estado_actual`):

    CONFIG   -- pantalla NES (configuracion_nes.py)
    JUGANDO  -- rondas de pato + disparo (tablero.py, partida.py, render_juego.py)
    FIN      -- por ahora solo imprime el resumen en consola; las próximas etapas
                agregan la ventana de resultados (Tkinter) y los gráficos finales.
"""
import sys

import pygame

import configuracion_nes as config_nes
import logica
import render_juego
from constantes import (
    ALTO_VENTANA,
    ANCHO_VENTANA,
    FPS,
    NEGRO,
    RUTA_PATO,
    RUTA_FONDO,
)
from partida import Ronda
from tablero import Tablero

RECT_TABLERO = pygame.Rect(30, 60, 900, 318)  # área de la ventana donde se dibuja el tablero


def ejecutar():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Duck Hunt -- Modo Jugable")
    reloj = pygame.time.Clock()

    fuente = pygame.font.SysFont("consolas", 26, bold=True)
    fuente_chica = pygame.font.SysFont("consolas", 16)

    estado_config = config_nes.crear_estado_inicial()
    estado_actual = "CONFIG"

    # Se inicializan cuando termina la configuración (necesitan TAM_GRID)
    tablero = None
    sprite_pato = None
    sprite_splash = None
    ronda_actual = None
    registros = []

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif estado_actual == "CONFIG":
                config_nes.manejar_evento(estado_config, evento)

            elif estado_actual == "JUGANDO" and evento.type == pygame.MOUSEBUTTONDOWN:
                ronda_actual.manejar_clic(evento.pos)

        # --- transición CONFIG -> JUGANDO ---
        if estado_actual == "CONFIG" and estado_config["confirmado"] and tablero is None:
            tam_grid = estado_config["grid"]
            tablero = Tablero(RUTA_FONDO, tam_grid, tam_grid, RECT_TABLERO)

            tam_sprite = tablero.tam_celda_pantalla()
            sprite_pato = render_juego.numpy_rgba_a_superficie(
                logica.cargar_sprite_sin_fondo(RUTA_PATO, tam_sprite)
            )
            sprite_splash = render_juego.numpy_rgba_a_superficie(
                logica.generar_mascara_splash(tam_sprite)
            )

            ronda_actual = Ronda(1, tablero)
            estado_actual = "JUGANDO"

        # --- lógica del estado JUGANDO ---
        if estado_actual == "JUGANDO":
            ronda_actual.actualizar()
            if ronda_actual.estado == Ronda.RESUELTA:
                registros.append(ronda_actual.registro())
                if ronda_actual.numero >= estado_config["disparos"]:
                    estado_actual = "FIN"
                else:
                    pygame.time.wait(500)  # una pausa breve para ver el resultado de la ronda
                    ronda_actual = Ronda(ronda_actual.numero + 1, tablero)

        # --- dibujo ---
        pantalla.fill(NEGRO)
        if estado_actual == "CONFIG":
            config_nes.dibujar(pantalla, estado_config, fuente, fuente_chica)

        elif estado_actual in ("JUGANDO", "FIN") and tablero is not None:
            tablero.dibujar_fondo(pantalla)
            tablero.dibujar_grid(pantalla)
            if estado_actual == "JUGANDO":
                render_juego.dibujar_pato(pantalla, tablero, ronda_actual, sprite_pato)
                render_juego.dibujar_resultado_ronda(pantalla, tablero, ronda_actual, sprite_splash)
                aciertos = sum(1 for r in registros if r["acierto"])
                render_juego.dibujar_hud(
                    pantalla, fuente_chica, ronda_actual, ronda_actual.numero,
                    estado_config["disparos"], aciertos,
                )

        pygame.display.flip()
        reloj.tick(FPS)

        if estado_actual == "FIN":
            corriendo = False

    if registros:
        aciertos = sum(1 for r in registros if r["acierto"])
        print(f"\nPartida terminada: {len(registros)} disparos, {aciertos} aciertos "
              f"({100 * aciertos / len(registros):.1f}%).")
        # Próxima etapa: ventana de resultados en Tkinter + CSV + gráficos.

    pygame.quit()


if __name__ == "__main__":
    ejecutar()
    sys.exit(0)
