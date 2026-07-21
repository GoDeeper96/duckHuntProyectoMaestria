# 🦆 Duck Hunt — Simulación en Python

Simulación simplificada del clásico videojuego **Duck Hunt**, desarrollada como proyecto de curso de **Programación 101** — Maestría en Ciencia de Datos e Inteligencia Artificial, UTEC. Profesor: **Royer Rojas Malasquez**.

Todo el proyecto vive en un único notebook: [`DuckHunt_Simulacion.ipynb`](./DuckHunt_Simulacion.ipynb).

<p align="center">
  <img src="docs/tablero_grid.png" width="720" alt="Tablero dividido en grid: color, escala de grises y blanco/negro">
</p>

## ¿Qué hace?

- Pantalla de configuración **estilo NES** (▲▼◄► + START) para elegir nombre de jugador, tamaño de grid y número de disparos — sin usar `input()`.
- Tablero dividido dinámicamente en una cuadrícula `n x n`, mostrado en color, escala de grises (fórmula de luminosidad calculada a mano con NumPy) y blanco/negro (umbral).
- `pato()`: aparece en una celda aleatoria (NumPy), con el fondo celeste de su sprite removido por **chroma-key** y pegado sobre el tablero con **mezcla alfa**.
- `pistola()`: dispara a una celda aleatoria y dibuja una mira vectorial (círculo + cruz) con Matplotlib.
- Validación de impacto: si pato y disparo coinciden → splash de sangre + pantalla **WINNER** + tono agudo sintetizado; si no → pantalla **GAME OVER** + tono grave.
- Bucle principal: juega los `N` disparos configurados completos (no se corta en el primer fallo).
- Pantalla final con el resumen de la partida, y registro en un **CSV histórico** (`registros_jugadores.csv`) que acumula todas las partidas de todos los jugadores.
- Estadísticas finales con pandas + Matplotlib + Seaborn: gráfico de barras, histograma, pie chart, heatmap de posiciones del pato, y un *leaderboard* comparando jugadores.

<p align="center">
  <img src="docs/pato_chromakey.png" width="720" alt="Pato pegado sobre el tablero sin el fondo celeste original">
</p>
<p align="center">
  <img src="docs/pantalla_winner.png" width="360" alt="Pantalla WINNER"> &nbsp;
  <img src="docs/pantalla_gameover.png" width="360" alt="Pantalla GAME OVER">
</p>
<p align="center">
  <img src="docs/graficos_estadisticos.png" width="720" alt="Gráficos de barras, histograma, pie chart y heatmap">
</p>

## Librerías usadas

| Librería | Para qué se usa aquí |
|---|---|
| **NumPy** | Posiciones aleatorias, matrices del tablero, conversión a grises/B-N, chroma-key, mezcla alfa, splash de sangre, síntesis de audio |
| **pandas** | Registro de cada disparo, resumen estadístico, CSV histórico, leaderboard |
| **Matplotlib** | Dibujo del tablero, la mira, las pantallas de reacción y los gráficos |
| **Seaborn** | Gráfico de barras, histograma y heatmap de la Sección 9 |
| **Pillow (PIL)** | Carga, recorte y redimensionado de imágenes/sprites |
| **ipywidgets** | Botones de la pantalla de configuración estilo NES |

## Estructura

```
FinalProjectP101/
├── DuckHunt_Simulacion.ipynb   # el proyecto completo, en 9 secciones
├── assets/
│   ├── paisaje-limpio (2).png  # fondo del tablero
│   ├── pato (1).png            # sprite del pato (fondo celeste sólido, se le quita con chroma-key)
│   ├── ganador.jpeg            # pantalla de acierto (WINNER)
│   └── gameover.jpg            # pantalla de fallo / fin de partida (GAME OVER)
├── docs/                       # capturas usadas en este README
├── requirements.txt
└── registros_jugadores.csv     # se genera solo al jugar (no está versionado, ver .gitignore)
```

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
jupyter notebook DuckHunt_Simulacion.ipynb
```

1. Corre las celdas **en orden, de arriba hacia abajo**.
2. En la **Sección 2** aparecen los botones ▲▼◄► y START: elige el nombre (solo A-Z), el tamaño de grid (3-8) y el número de disparos (5-99), y presiona **START**. Las celdas siguientes dependen de esta configuración.
3. La **Sección 7** (bucle principal) genera varias figuras y un sonido por cada disparo — con 20 disparos por defecto, tarda unos segundos en terminar.
4. Al final (secciones 8 y 9) se muestra la pantalla de resultados, se guarda la partida en `registros_jugadores.csv`, y se generan los gráficos estadísticos.

## Notas de diseño

- **`pato (1).png` no tenía transparencia real** — tenía un fondo celeste sólido "horneado" en el archivo. Se detectó inspeccionando el canal alfa con NumPy y se resolvió con una función de *chroma-key* (Sección 4).
- El **splash de sangre** y la **mira del disparo** se generan por código (círculos con NumPy), no son imágenes — mismo criterio para "manipulación de imágenes" que usa fórmulas explícitas en vez de funciones de conveniencia de una librería.
- El **audio** (aciertos/fallos) se sintetiza con ondas senoidales de NumPy (`IPython.display.Audio`), porque no había archivos de sonido en el proyecto.

## Pendiente para el equipo

Del enunciado original, esto todavía no está cubierto por el notebook:

- [ ] Informe técnico en PDF
- [ ] Capturas de ejecución adicionales para el informe
- [ ] Exposición en clase
- [ ] Video corto de demostración (opcional)
