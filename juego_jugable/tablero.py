# -*- coding: utf-8 -*-
"""
El tablero: carga el fondo, lo convierte a la versión en grises (misma regla que el
notebook: el enunciado solo pide blanco/negro o escala de grises), arma la cuadrícula,
y traduce coordenadas entre "píxel de la ventana" y "celda del grid".

Por qué una clase y no funciones sueltas: el tablero se dibuja *escalado* dentro de la
ventana (la imagen original es de 1920x678 px, mucho más grande que la ventana de
juego), así que necesitamos recordar la escala y la posición donde se dibuja para poder
convertir un clic del mouse (coordenadas de pantalla) de vuelta a una celda del grid
(coordenadas de la imagen original). Guardar eso en atributos de instancia evita pasar
5 parámetros sueltos a cada función.
"""
import numpy as np
import pygame

import logica


class Tablero:
    def __init__(self, ruta_fondo, filas, columnas, rect_pantalla):
        color = logica.cargar_fondo(ruta_fondo)
        grises = logica.convertir_a_grises(color)
        # FONDO_JUEGO: escala de grises expandida a 3 canales, igual que en el notebook,
        # para que los sprites de color (pato, splash) resalten sobre un fondo acromático.
        self.imagen = np.stack([grises] * 3, axis=-1)

        self.alto_img, self.ancho_img = self.imagen.shape[0], self.imagen.shape[1]
        self.filas, self.columnas = filas, columnas
        self.bordes_fila, self.bordes_columna = logica.construir_bordes_grid(
            self.alto_img, self.ancho_img, filas, columnas
        )

        self.rect_pantalla = rect_pantalla
        self.escala_x = rect_pantalla.width / self.ancho_img
        self.escala_y = rect_pantalla.height / self.alto_img

        superficie_base = self._numpy_a_superficie(self.imagen)
        self._superficie_escalada = pygame.transform.smoothscale(
            superficie_base, (rect_pantalla.width, rect_pantalla.height)
        )

    @staticmethod
    def _numpy_a_superficie(imagen_rgb):
        # pygame.surfarray indexa las superficies como [x, y] (columna-mayor);
        # NumPy guarda imágenes como [fila, columna] = [y, x] (fila-mayor).
        # Sin este transpose la imagen sale rotada 90° y espejada.
        return pygame.surfarray.make_surface(np.transpose(imagen_rgb, (1, 0, 2)))

    def dibujar_fondo(self, pantalla):
        pantalla.blit(self._superficie_escalada, self.rect_pantalla.topleft)

    def dibujar_grid(self, pantalla, color=(200, 40, 40)):
        for fila_px in self.bordes_fila:
            y = self.rect_pantalla.top + int(fila_px * self.escala_y)
            pygame.draw.line(pantalla, color, (self.rect_pantalla.left, y), (self.rect_pantalla.right, y))
        for col_px in self.bordes_columna:
            x = self.rect_pantalla.left + int(col_px * self.escala_x)
            pygame.draw.line(pantalla, color, (x, self.rect_pantalla.top), (x, self.rect_pantalla.bottom))

    def centro_celda_pantalla(self, fila, columna):
        """Centro de la celda (fila, columna) en coordenadas de PANTALLA (para ubicar sprites)."""
        x_img, y_img = logica.centro_celda(fila, columna, self.bordes_fila, self.bordes_columna)
        return (
            self.rect_pantalla.left + int(x_img * self.escala_x),
            self.rect_pantalla.top + int(y_img * self.escala_y),
        )

    def celda_en_click(self, pos_click):
        """Convierte un clic (coordenadas de PANTALLA) al índice de celda, o None si cae fuera del tablero."""
        x_click, y_click = pos_click
        if not self.rect_pantalla.collidepoint(x_click, y_click):
            return None
        x_img = (x_click - self.rect_pantalla.left) / self.escala_x
        y_img = (y_click - self.rect_pantalla.top) / self.escala_y
        return logica.celda_en_pixel(x_img, y_img, self.bordes_fila, self.bordes_columna)

    def tam_celda_pantalla(self):
        """Tamaño aproximado (px de pantalla) de una celda, para dimensionar sprites."""
        ancho_celda = (self.bordes_columna[1] - self.bordes_columna[0]) * self.escala_x
        alto_celda = (self.bordes_fila[1] - self.bordes_fila[0]) * self.escala_y
        return int(min(ancho_celda, alto_celda))
