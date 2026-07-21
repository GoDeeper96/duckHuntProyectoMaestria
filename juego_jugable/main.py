# -*- coding: utf-8 -*-
"""
Punto de entrada del modo jugable.

Estados del juego (máquina de estados simple, un string en `estado_actual`):

    CONFIG   -- pantalla NES (configuracion_nes.py)
    JUGANDO  -- rondas de pato + disparo (tablero.py, partida.py, render_juego.py, audio.py)
    FIN      -- pygame se cierra y el control pasa a Tkinter (resultados_tkinter.py)
                y luego a Matplotlib/Seaborn (graficos.py) -- dos motores de UI
                distintos no pueden compartir el mismo bucle de eventos, así que
                se ejecutan en secuencia, no al mismo tiempo.
"""
import sys

import pandas as pd
import pygame

import audio
import configuracion_nes as config_nes
import graficos
import logica
import render_juego
import resultados_tkinter
from constantes import (
    ALTO_VENTANA,
    ANCHO_VENTANA,
    FPS,
    NEGRO,
    RUTA_FONDO,
    RUTA_PATO,
)
from partida import Ronda
from tablero import Tablero

RECT_TABLERO = pygame.Rect(30, 60, 900, 318)  # área de la ventana donde se dibuja el tablero


def ejecutar():
    pygame.init()
    audio.inicializar_audio()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Duck Hunt -- Modo Jugable")
    reloj = pygame.time.Clock()

    fuente = pygame.font.SysFont("consolas", 26, bold=True)
    fuente_chica = pygame.font.SysFont("consolas", 16)

    estado_config = config_nes.crear_estado_inicial()
    estado_actual = "CONFIG"

    tablero = None
    sprite_pato = None
    sprite_splash = None
    ronda_actual = None
    registros = []

    corriendo = True
    while corriendo:
        recien_resuelta = False  # ¿la ronda actual se resolvió en ESTA vuelta del bucle?

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif estado_actual == "CONFIG":
                config_nes.manejar_evento(estado_config, evento)

            elif estado_actual == "JUGANDO" and evento.type == pygame.MOUSEBUTTONDOWN:
                if ronda_actual.manejar_clic(evento.pos):
                    recien_resuelta = True

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
            if ronda_actual.actualizar():  # True si se acaba de agotar el tiempo
                recien_resuelta = True

            if recien_resuelta:
                registros.append(ronda_actual.registro())
                (audio.sonido_acierto if ronda_actual.acierto else audio.sonido_fallo)()

        # --- dibujo ---
        # Importante: se dibuja ANTES de reemplazar ronda_actual por la siguiente ronda,
        # para que el jugador alcance a ver el splash/X del resultado en pantalla (si el
        # reemplazo pasara antes de este bloque, el resultado nunca llegaría a mostrarse).
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

        # --- avanzar a la siguiente ronda (después de haber mostrado el resultado) ---
        if estado_actual == "JUGANDO" and recien_resuelta:
            if ronda_actual.numero >= estado_config["disparos"]:
                estado_actual = "FIN"
            else:
                pygame.time.wait(500)  # pausa para que se alcance a ver el resultado ya dibujado
                ronda_actual = Ronda(ronda_actual.numero + 1, tablero)

        if estado_actual == "FIN":
            corriendo = False

    tam_grid_final = estado_config["grid"]
    nombre_jugador = config_nes.obtener_nombre_actual(estado_config)
    pygame.quit()  # liberamos ventana y audio de pygame antes de abrir Tkinter

    if not registros:
        return  # el jugador cerró la ventana antes de terminar la partida

    estadisticas = logica.calcular_estadisticas(registros, nombre_jugador, tam_grid_final)
    print(f"\nPartida terminada: {estadisticas['total_disparos']} disparos, "
          f"{estadisticas['disparos_exitosos']} aciertos ({estadisticas['porcentaje_aciertos']}%).")

    resultados_tkinter.mostrar_resultados(estadisticas)

    graficos.guardar_registro_csv(estadisticas)
    graficos.graficar_leaderboard(graficos.cargar_historial())
    graficos.graficar_resultado_partida(pd.DataFrame(registros), estadisticas, tam_grid_final)


if __name__ == "__main__":
    ejecutar()
    sys.exit(0)
