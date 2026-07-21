# -*- coding: utf-8 -*-
"""
Una Ronda = un pato que aparece en una celda al azar + el intento de disparo del
jugador (clic o tiempo agotado). Se modela como una máquina de estados de 2 pasos:

    ESPERANDO_CLIC  --(clic dentro del tablero, o se acaba el tiempo)-->  RESUELTA

Separar esto en su propia clase (en vez de mezclarlo con el bucle principal de
main.py) es lo que permite testear "¿qué pasa si el jugador le acierta?" o
"¿qué pasa si no dispara a tiempo?" llamando directamente a estos métodos, sin
necesitar una ventana de pygame ni un mouse real.
"""
import time

import logica
from constantes import TIEMPO_LIMITE_PATO


class Ronda:
    ESPERANDO_CLIC = "esperando_clic"
    RESUELTA = "resuelta"

    def __init__(self, numero, tablero, tiempo_limite=TIEMPO_LIMITE_PATO, reloj=time.time):
        self.numero = numero
        self.tablero = tablero
        self.tiempo_limite = tiempo_limite
        self._reloj = reloj  # inyectable para poder testear sin esperar el tiempo real

        self.posicion_pato = logica.generar_posicion_aleatoria(tablero.filas, tablero.columnas)
        self._hora_inicio = self._reloj()
        self.estado = Ronda.ESPERANDO_CLIC
        self.acierto = None
        self.posicion_disparo = None
        self.a_tiempo = None  # False si se resolvió porque se acabó el tiempo (no hubo clic válido)

    def tiempo_restante(self):
        transcurrido = self._reloj() - self._hora_inicio
        return max(0.0, self.tiempo_limite - transcurrido)

    def manejar_clic(self, pos_pantalla):
        """
        pos_pantalla: coordenadas de pantalla del clic (píxeles de la ventana).
        Devuelve True si este clic fue el que resolvió la ronda ahora mismo -- main.py
        usa ese aviso directo para saber cuándo registrar el resultado y pasar a la
        siguiente ronda, en vez de comparar el estado de "antes" contra el de "después"
        (comparación que se rompía porque el clic se procesa en medio del bucle de
        eventos, antes de que el resto del loop pudiera notar el cambio).
        """
        if self.estado != Ronda.ESPERANDO_CLIC:
            return False
        celda = self.tablero.celda_en_click(pos_pantalla)
        if celda is None:
            return False  # clic fuera del tablero: no cuenta como intento
        self._resolver(celda, a_tiempo=True)
        return True

    def actualizar(self):
        """Devuelve True si el tiempo se acaba de agotar y la ronda quedó resuelta recién."""
        if self.estado == Ronda.ESPERANDO_CLIC and self.tiempo_restante() <= 0:
            self._resolver(posicion_disparo=None, a_tiempo=False)
            return True
        return False

    def _resolver(self, posicion_disparo, a_tiempo):
        self.posicion_disparo = posicion_disparo
        self.a_tiempo = a_tiempo
        self.acierto = logica.validar_impacto(self.posicion_pato, posicion_disparo)
        self.estado = Ronda.RESUELTA

    def registro(self):
        disparo_fila = self.posicion_disparo[0] if self.posicion_disparo else None
        disparo_columna = self.posicion_disparo[1] if self.posicion_disparo else None
        return {
            "disparo_num": self.numero,
            "pato_fila": self.posicion_pato[0],
            "pato_columna": self.posicion_pato[1],
            "disparo_fila": disparo_fila,
            "disparo_columna": disparo_columna,
            "a_tiempo": self.a_tiempo,
            "acierto": bool(self.acierto),
        }
