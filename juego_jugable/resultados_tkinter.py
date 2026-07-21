# -*- coding: utf-8 -*-
"""
Ventana de resultados en Tkinter, mostrada al terminar la partida.

Va en un módulo separado (y usa un motor de UI distinto al del juego) a propósito:
mientras se juega, pygame necesita control total del bucle de eventos para que el
tablero responda en tiempo real; una vez terminada la partida ya no hace falta esa
inmediatez, así que usamos un widget nativo del sistema operativo (Tkinter, incluido
en Python estándar) para una ventana de resumen simple, en vez de seguir dibujando
texto a mano con pygame.font.
"""
import tkinter as tk

NEGRO = "#101010"
VERDE = "#39ff14"
AMARILLO = "#ffdd00"
GRIS = "#aaaaaa"


def mostrar_resultados(estadisticas, bloquear=True):
    """
    Construye la ventana de resumen. Con bloquear=True corre ventana.mainloop()
    (uso normal: se espera a que el jugador la cierre). Con bloquear=False se
    arma la ventana y se hace un solo update() sin entrar al mainloop -- se usa
    para probar que los widgets se construyen bien sin abrir una ventana real.
    """
    ventana = tk.Tk()
    ventana.title("Duck Hunt -- Resultados")
    ventana.configure(bg=NEGRO)
    ventana.resizable(False, False)

    tk.Label(
        ventana, text="FIN DE LA PARTIDA", font=("Consolas", 18, "bold"),
        fg=VERDE, bg=NEGRO,
    ).grid(row=0, column=0, columnspan=2, padx=30, pady=(18, 12))

    filas = [
        ("Jugador", estadisticas["jugador"]),
        ("Grid", estadisticas["grid"]),
        ("Disparos totales", estadisticas["total_disparos"]),
        ("Aciertos", f"{estadisticas['disparos_exitosos']} ({estadisticas['porcentaje_aciertos']}%)"),
        ("Fallos", f"{estadisticas['disparos_errados']} ({estadisticas['porcentaje_fallos']}%)"),
    ]
    for i, (etiqueta, valor) in enumerate(filas, start=1):
        tk.Label(
            ventana, text=etiqueta, font=("Consolas", 12), fg=GRIS, bg=NEGRO, anchor="w",
        ).grid(row=i, column=0, sticky="w", padx=(30, 10), pady=4)
        tk.Label(
            ventana, text=str(valor), font=("Consolas", 12, "bold"), fg=AMARILLO, bg=NEGRO, anchor="w",
        ).grid(row=i, column=1, sticky="w", padx=(0, 30), pady=4)

    tk.Button(
        ventana, text="Ver gráficos y cerrar", command=ventana.destroy,
        font=("Consolas", 11, "bold"), bg=VERDE, fg="#000000",
    ).grid(row=len(filas) + 1, column=0, columnspan=2, pady=18)

    if bloquear:
        ventana.mainloop()
    else:
        ventana.update()
        ventana.destroy()
