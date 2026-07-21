# -*- coding: utf-8 -*-
"""
Estadísticas finales: los mismos 4 gráficos que pide el enunciado (barras,
histograma, pie chart, heatmap) más el leaderboard -- misma lógica que la
Sección 9 del notebook, adaptada para mostrarse con plt.show() en vez de
quedar embebida en una celda.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from constantes import RUTA_CSV_REGISTROS


def agregar_columna_distancia(df):
    """
    Distancia euclidiana entre el pato y el disparo. En el modo jugable un disparo
    puede no existir (se acabó el tiempo sin clic), así que esas filas quedan con
    distancia NaN en vez de forzar un valor -- no hay disparo real que medir.
    """
    df = df.copy()
    con_disparo = df["disparo_fila"].notna()
    df["distancia"] = np.nan
    df.loc[con_disparo, "distancia"] = np.sqrt(
        (df.loc[con_disparo, "pato_fila"] - df.loc[con_disparo, "disparo_fila"]) ** 2
        + (df.loc[con_disparo, "pato_columna"] - df.loc[con_disparo, "disparo_columna"]) ** 2
    )
    return df


def construir_matriz_frecuencia_pato(df, tam_grid):
    matriz = np.zeros((tam_grid, tam_grid), dtype=int)
    np.add.at(matriz, (df["pato_fila"], df["pato_columna"]), 1)
    return matriz


def graficar_resultado_partida(df_registros, estadisticas, tam_grid):
    """Panel 2x2: barras, histograma de distancia, pie chart y heatmap de posiciones del pato."""
    sns.set_theme(style="whitegrid")
    df = agregar_columna_distancia(df_registros)
    matriz = construir_matriz_frecuencia_pato(df, tam_grid)

    fig, ejes = plt.subplots(2, 2, figsize=(11, 9))

    conteo = df["acierto"].map({True: "Acierto", False: "Fallo"}).value_counts()
    sns.barplot(x=conteo.index, y=conteo.values, hue=conteo.index,
                palette={"Acierto": "seagreen", "Fallo": "indianred"}, legend=False, ax=ejes[0, 0])
    ejes[0, 0].set_title("Aciertos vs. fallos")
    ejes[0, 0].set_xlabel("")
    ejes[0, 0].set_ylabel("Cantidad de disparos")

    distancias = df["distancia"].dropna()
    if len(distancias) > 0:
        sns.histplot(distancias, bins=8, color="steelblue", ax=ejes[0, 1])
    ejes[0, 1].set_title("Distancia pato-disparo (solo clics, sin tiempos agotados)")
    ejes[0, 1].set_xlabel("Distancia (celdas)")
    ejes[0, 1].set_ylabel("Frecuencia")

    valores = [estadisticas["disparos_exitosos"], estadisticas["disparos_errados"]]
    etiquetas = [f"Aciertos ({estadisticas['porcentaje_aciertos']}%)",
                 f"Fallos ({estadisticas['porcentaje_fallos']}%)"]
    ejes[1, 0].pie(valores, labels=etiquetas, colors=["seagreen", "indianred"],
                    autopct=lambda p: f"{p:.0f}%" if p > 0 else "", startangle=90)
    ejes[1, 0].set_title("Proporción de aciertos")

    sns.heatmap(matriz, annot=True, fmt="d", cmap="Reds", cbar=True, ax=ejes[1, 1])
    ejes[1, 1].set_title("Frecuencia de aparición del pato por celda")
    ejes[1, 1].set_xlabel("Columna")
    ejes[1, 1].set_ylabel("Fila")

    plt.tight_layout()
    plt.show()


def guardar_registro_csv(estadisticas, ruta_csv=RUTA_CSV_REGISTROS):
    """Agrega una fila al CSV histórico del modo jugable (lo crea si no existe)."""
    ruta_csv.parent.mkdir(parents=True, exist_ok=True)
    fila = pd.DataFrame([{**estadisticas, "fecha_hora": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}])
    escribir_encabezado = not ruta_csv.exists()
    fila.to_csv(ruta_csv, mode="a", header=escribir_encabezado, index=False, encoding="utf-8")
    print(f"Registro guardado en '{ruta_csv}'.")


def cargar_historial(ruta_csv=RUTA_CSV_REGISTROS):
    if not ruta_csv.exists():
        return pd.DataFrame()
    return pd.read_csv(ruta_csv)


def graficar_leaderboard(historial):
    """Tabla + gráfico de barras comparando todas las partidas jugables registradas."""
    if historial.empty:
        print("Todavía no hay historial de partidas jugables registradas.")
        return

    leaderboard = historial.sort_values("porcentaje_aciertos", ascending=False).reset_index(drop=True)
    print("\nHistorial de partidas (modo jugable):")
    print(leaderboard.to_string(index=False))

    etiquetas = leaderboard["jugador"] + " (" + leaderboard["fecha_hora"].str.slice(0, 16) + ")"
    fig, ax = plt.subplots(figsize=(9, max(3, 0.5 * len(leaderboard))))
    sns.barplot(x=leaderboard["porcentaje_aciertos"], y=etiquetas, hue=etiquetas,
                palette="viridis", legend=False, ax=ax)
    ax.set_title("Leaderboard (modo jugable) -- % de aciertos por partida")
    ax.set_xlabel("% de aciertos")
    ax.set_ylabel("")
    ax.set_xlim(0, 100)
    plt.tight_layout()
    plt.show()
