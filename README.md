# 🦆 Duck Hunt — Simulación en Python

Proyecto de curso de **Programación 101** — Maestría en Ciencia de Datos e Inteligencia Artificial, UTEC. Profesor: **Royer Rojas Malasquez**.

Todo el proyecto vive en un único notebook: **[`DuckHunt_Simulacion.ipynb`](./DuckHunt_Simulacion.ipynb)**. `pato()` y `pistola()` generan sus posiciones al azar (NumPy), y el proyecto se evalúa sobre esto (NumPy, pandas, Matplotlib y Seaborn son las librerías obligatorias).

<p align="center">
  <img src="docs/tablero_grid.png" width="720" alt="Tablero en escala de grises dividido en grid">
</p>

## ¿Qué hace?

- Configuración de partida por teclado: `input()` pide nombre, número de disparos y tamaño de grid (`NUM_DISPAROS`/`TAM_GRID` se convierten con `int()`), y `validar_configuracion()` avisa con un mensaje claro si algún valor no es válido — tal como pide el enunciado ("El valor de n debe ser configurable").
- Tablero dividido dinámicamente en una cuadrícula `n x n`. El enunciado pide mostrar el fondo en blanco/negro o escala de grises, así que **todo el proyecto usa únicamente escala de grises** (fórmula de luminosidad calculada a mano con NumPy) — no se muestra ni se juega en color.
- `pato()`: aparece en una celda aleatoria (NumPy) y se dibuja con `ax.imshow(sprite, extent=[...])` — Matplotlib compone la transparencia del PNG automáticamente, así que no hace falta mezclar píxeles a mano. El sprite necesita **chroma-key** porque `pato.png` no trae transparencia real (tiene un fondo celeste sólido "horneado" en el archivo); ese chroma-key se aplicó una sola vez, de antemano (ver "Notas de diseño" abajo).
- `pistola()`: dispara a una celda aleatoria y marca la celda con un `Rectangle` (borde) + un marcador `"x"` de Matplotlib, en vez de calcular una mira a mano.
- Validación de impacto: si pato y disparo coinciden → pantalla **WINNER**; si no → pantalla **GAME OVER**.
- Bucle principal: juega los `N` disparos configurados completos (no se corta en el primer fallo); cada ronda dibuja un solo tablero con el pato y la mira juntos.
- Pantalla final con el resumen de la partida, y registro en un **CSV histórico** (`registros_jugadores.csv`) que acumula todas las partidas de todos los jugadores.
- Estadísticas finales con pandas + Matplotlib + Seaborn: gráfico de barras, pie chart, heatmap de posiciones del pato, y un *leaderboard* comparando jugadores.

<p align="center">
  <img src="docs/pato_chromakey.png" width="720" alt="Pato y mira dibujados juntos sobre el tablero en escala de grises">
</p>
<p align="center">
  <img src="docs/pantalla_winner.png" width="360" alt="Pantalla WINNER"> &nbsp;
  <img src="docs/pantalla_gameover.png" width="360" alt="Pantalla GAME OVER">
</p>
<p align="center">
  <img src="docs/graficos_estadisticos.png" width="720" alt="Gráficos de barras, pie chart y heatmap">
</p>

## Librerías usadas

| Librería | Para qué se usa aquí |
|---|---|
| **NumPy** | Posiciones aleatorias, matrices del tablero, conversión a grises, geometría del grid |
| **pandas** | Registro de cada disparo, resumen estadístico, CSV histórico, leaderboard |
| **Matplotlib** | Dibujo del tablero, la mira, las pantallas de reacción y los gráficos |
| **Seaborn** | Gráfico de barras, pie chart y heatmap de la Sección 9 |
| **Pillow (PIL)** | Carga de imágenes/sprites |

Explicación detallada de por qué se eligió cada una, con ejemplos del código: **[`LIBRERIAS.md`](./LIBRERIAS.md)**.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
jupyter notebook DuckHunt_Simulacion.ipynb
```

1. Corre las celdas **en orden, de arriba hacia abajo**.
2. En la **Sección 2** el notebook pide por teclado el nombre del jugador, el número de disparos (5-99) y el tamaño de grid (3-8) — escribí la respuesta en el cuadro de texto que aparece arriba del notebook y presioná Enter. `validar_configuracion()` avisa con un mensaje claro si algún valor queda fuera de rango.
3. La **Sección 7** (bucle principal) genera dos figuras por disparo (el tablero de la ronda y la pantalla de reacción) — con 20 disparos por defecto, tarda unos segundos en terminar.
4. Al final (secciones 8 y 9) se muestra la pantalla de resultados, se guarda la partida en `registros_jugadores.csv`, y se generan los gráficos estadísticos.

## Notas de diseño

- **`pato (1).png` no tenía transparencia real** — tenía un fondo celeste sólido "horneado" en el archivo. Se detectó inspeccionando el canal alfa con NumPy (`np.unique(arr[...,3])` daba solo `255`), y se resolvió con chroma-key aplicado **una sola vez, fuera del notebook**: `assets/pato_limpio.png` ya viene con el fondo quitado, así el código de `pato()` no necesita explicar ni ejecutar ese preprocesamiento cada vez.
- **`pato()` y `pistola()` dibujan con `ax.imshow(imagen, extent=[...])`**: Matplotlib compone la transparencia de un PNG automáticamente al dibujarlo como una capa sobre los ejes, así que no hace falta escribir una fórmula de mezcla alfa a mano. `extent` define en qué rectángulo del tablero se dibuja la imagen, calculado para conservar la proporción original del sprite dentro de la celda.
- Sin audio ni splash de sangre: se sacaron del notebook para mantener `pato()`/`pistola()`/la validación de impacto simples y enfocadas en lo que pide el enunciado.

## Documentación del proyecto

- **[`INFORME_TECNICO.md`](./INFORME_TECNICO.md) / [`INFORME_TECNICO.pdf`](./INFORME_TECNICO.pdf)** — informe técnico completo: objetivos, arquitectura, funcionalidades, capturas, análisis estadístico y decisiones de diseño.
- **[`LIBRERIAS.md`](./LIBRERIAS.md)** — por qué se usó cada librería (NumPy, pandas, Matplotlib, Seaborn, Pillow), con ejemplos del código real.
- **[`docs/GUION_VIDEO.md`](./docs/GUION_VIDEO.md)** — guion para grabar el video de exposición.

## Pendiente para el equipo

Del enunciado original, esto todavía no está cubierto:

- [ ] Completar los nombres del equipo en `INFORME_TECNICO.md`
- [ ] Exposición en clase
- [ ] Video corto de demostración (opcional)
