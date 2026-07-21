# -*- coding: utf-8 -*-
"""
Pantalla de configuración estilo NES — versión con teclado real.

Es la misma idea que la Sección 2 del notebook (nombre + grid + disparos como una
sola fila de "casillas" editables, con un cursor plano que las recorre), pero acá
las flechas ARROW_UP/DOWN/LEFT/RIGHT son eventos reales de teclado (pygame.KEYDOWN),
no botones que hay que clickear -- Jupyter no puede capturar teclas físicas de forma
confiable, un juego de escritorio sí.

Como en el notebook, se separa en tres capas:
  - estado y funciones puras (testeables sin abrir ninguna ventana)
  - manejar_evento() (traduce un evento de pygame a un cambio de estado)
  - dibujar() (la única función que depende de pygame.font / pygame.draw)
"""
import pygame

from constantes import (
    ALFABETO_NES,
    AMARILLO,
    DISPAROS_MAX,
    DISPAROS_MIN,
    GRID_MAX,
    GRID_MIN,
    NEGRO,
    NOMBRE_MAX_LEN,
    ROJO,
    VERDE_NES,
)

TOTAL_CASILLAS = NOMBRE_MAX_LEN + 2
CASILLA_GRID = NOMBRE_MAX_LEN
CASILLA_DISPAROS = NOMBRE_MAX_LEN + 1


# ============================================================
# ESTADO Y LÓGICA PURA (sin pygame)
# ============================================================
def crear_estado_inicial():
    return {
        "letras": ["_"] * NOMBRE_MAX_LEN,
        "grid": 4,
        "disparos": 20,
        "cursor": 0,
        "confirmado": False,
        "error": "",
    }


def limitar(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def mover_cursor(estado, direccion):
    estado["cursor"] = (estado["cursor"] + direccion) % TOTAL_CASILLAS


def cambiar_valor(estado, direccion):
    cursor = estado["cursor"]
    if cursor < NOMBRE_MAX_LEN:
        idx_actual = ALFABETO_NES.index(estado["letras"][cursor])
        estado["letras"][cursor] = ALFABETO_NES[(idx_actual + direccion) % len(ALFABETO_NES)]
    elif cursor == CASILLA_GRID:
        estado["grid"] = limitar(estado["grid"] + direccion, GRID_MIN, GRID_MAX)
    elif cursor == CASILLA_DISPAROS:
        estado["disparos"] = limitar(estado["disparos"] + direccion, DISPAROS_MIN, DISPAROS_MAX)


def obtener_nombre_actual(estado):
    return "".join(letra for letra in estado["letras"] if letra != "_")


def validar_configuracion(estado):
    if len(obtener_nombre_actual(estado)) == 0:
        return False, "El nombre no puede estar vacío. Usa las flechas para elegir letras."
    return True, ""


def intentar_confirmar(estado):
    """Intenta cerrar la pantalla de configuración. Devuelve True si quedó confirmada."""
    es_valido, mensaje = validar_configuracion(estado)
    if not es_valido:
        estado["error"] = mensaje
        return False
    estado["confirmado"] = True
    return True


# ============================================================
# EVENTOS (traduce teclado -> cambios de estado)
# ============================================================
def manejar_evento(estado, evento):
    """Procesa un evento de pygame. Devuelve True si la configuración quedó confirmada."""
    if estado["confirmado"]:
        return True
    if evento.type != pygame.KEYDOWN:
        return False

    estado["error"] = ""
    if evento.key == pygame.K_LEFT:
        mover_cursor(estado, -1)
    elif evento.key == pygame.K_RIGHT:
        mover_cursor(estado, +1)
    elif evento.key == pygame.K_UP:
        cambiar_valor(estado, +1)
    elif evento.key == pygame.K_DOWN:
        cambiar_valor(estado, -1)
    elif evento.key == pygame.K_RETURN:
        return intentar_confirmar(estado)
    return False


# ============================================================
# DIBUJO (única parte que depende de pygame.font / pygame.draw)
# ============================================================
def dibujar(pantalla, estado, fuente, fuente_chica):
    pantalla.fill(NEGRO)

    titulo = fuente.render("=== CONFIGURACION DE PARTIDA ===", True, VERDE_NES)
    pantalla.blit(titulo, (60, 60))

    ayuda = fuente_chica.render(
        "FLECHAS izq/der: mover cursor   FLECHAS arriba/abajo: cambiar valor   ENTER: confirmar",
        True, (170, 170, 170),
    )
    pantalla.blit(ayuda, (60, 100))

    # --- fila del nombre: una casilla por letra ---
    y_nombre = 180
    for i, letra in enumerate(estado["letras"]):
        activa = estado["cursor"] == i
        color_fondo = VERDE_NES if activa else NEGRO
        color_texto = NEGRO if activa else VERDE_NES
        rect = pygame.Rect(60 + i * 36, y_nombre, 32, 40)
        pygame.draw.rect(pantalla, color_fondo, rect)
        pygame.draw.rect(pantalla, VERDE_NES, rect, width=1)
        texto = fuente.render(letra, True, color_texto)
        pantalla.blit(texto, texto.get_rect(center=rect.center))

    # --- grid y disparos ---
    y_campos = 260
    _dibujar_campo(pantalla, fuente, f"GRID: {estado['grid']} x {estado['grid']}",
                    60, y_campos, estado["cursor"] == CASILLA_GRID)
    _dibujar_campo(pantalla, fuente, f"DISPAROS: {estado['disparos']:02d}",
                    60, y_campos + 60, estado["cursor"] == CASILLA_DISPAROS)

    # --- mensajes ---
    if estado["confirmado"]:
        nombre = obtener_nombre_actual(estado)
        msg = fuente_chica.render(
            f"LISTO -- JUGADOR: {nombre} | GRID {estado['grid']}x{estado['grid']} | "
            f"{estado['disparos']} DISPAROS", True, AMARILLO,
        )
        pantalla.blit(msg, (60, 400))
    elif estado["error"]:
        msg = fuente_chica.render(estado["error"], True, ROJO)
        pantalla.blit(msg, (60, 400))


def _dibujar_campo(pantalla, fuente, texto, x, y, activo):
    color_fondo = VERDE_NES if activo else NEGRO
    color_texto = NEGRO if activo else VERDE_NES
    superficie = fuente.render(texto, True, color_texto)
    rect = superficie.get_rect(topleft=(x, y)).inflate(16, 10)
    pygame.draw.rect(pantalla, color_fondo, rect)
    pygame.draw.rect(pantalla, VERDE_NES, rect, width=1)
    pantalla.blit(superficie, (x, y))
