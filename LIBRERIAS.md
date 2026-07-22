# Por qué usamos cada librería

Este documento explica, librería por librería, qué rol cumple en el proyecto y por qué la elegimos — no es una lista genérica de "para qué sirve NumPy en general", sino específicamente qué hace **en este notebook**, con ejemplos tomados del código real.

El enunciado exige explícitamente cuatro librerías (NumPy, pandas, Matplotlib, Seaborn); además usamos Pillow como apoyo para cargar imágenes.

---

## NumPy — matrices, cuadrículas y aleatoriedad

NumPy es el corazón matemático del proyecto. Lo usamos para todo lo que implica trabajar con una imagen o una posición como una matriz de números, no como un objeto abstracto.

**Dónde se usa:**

- **Conversión a escala de grises** (`convertir_a_grises`): una imagen a color es una matriz `(alto, ancho, 3)`. Con `np.dot(imagen[..., :3], [0.299, 0.587, 0.114])` aplicamos la fórmula de luminosidad a **todos los píxeles a la vez**, sin escribir un bucle `for` que recorra la imagen píxel por píxel. Esto es exactamente la clase de operación para la que NumPy existe: reemplazar bucles explícitos por operaciones vectorizadas sobre arreglos completos.
- **Generación de la cuadrícula** (`construir_bordes_grid`): `np.linspace(0, ancho, columnas + 1)` calcula de una sola vez los límites en píxeles de cada columna del grid, en vez de calcularlos uno por uno con aritmética manual.
- **Aleatoriedad** (`generar_posicion_aleatoria`): `np.random.randint(0, filas)` es la fuente de azar que usan tanto `pato()` como `pistola()` para elegir una celda — es el requisito de "generación de números aleatorios" del enunciado, aplicado directamente a la lógica del juego.
- **Las matrices del heatmap** (`construir_matrices_resultado`): dos arreglos `TAM_GRID x TAM_GRID` de ceros (uno para aciertos, otro para fallos) que se van incrementando con `np.add.at(matriz, (filas, columnas), 1)` — la misma idea de "una matriz que representa el tablero" que se usó para el fondo, ahora usada para contar resultados por celda.

**Por qué esta y no otra:** no hay alternativa razonable — es la librería estándar de Python para álgebra matricial y arreglos numéricos, y es la que pide el enunciado explícitamente para "manejo de matrices, cuadrículas y números aleatorios".

---

## pandas — registro y análisis de los disparos

pandas entra en escena después de que el juego ya generó datos: convierte una lista de resultados sueltos en una tabla que se puede analizar.

**Dónde se usa:**

- **Armar la tabla de la partida**: `pd.DataFrame(REGISTROS_PARTIDA)` convierte la lista de diccionarios (uno por disparo, con `pato_fila`, `pato_columna`, `disparo_fila`, `disparo_columna`, `acierto`) en una tabla real, con columnas con nombre y filas indexadas.
- **Calcular el resumen** (`calcular_estadisticas`): `df_partida["acierto"].sum()` cuenta los aciertos sumando una columna de booleanos (`True` se comporta como `1`) — una operación de una sola línea en vez de un bucle contando manualmente.
- **El CSV histórico** (`guardar_registro_csv` / `cargar_historial`): `DataFrame.to_csv(..., mode="a")` agrega una fila nueva al archivo sin reescribir las partidas anteriores, y `pd.read_csv(...)` lo vuelve a leer como tabla para armar el leaderboard. Esto es "registro y análisis estadístico de disparos" tal como lo pide el enunciado, incluyendo la persistencia entre distintas ejecuciones del notebook.

**Por qué esta y no otra:** pandas es el estándar de facto en Python para tablas de datos (equivalente a una hoja de cálculo programable), y es la librería que el enunciado exige específicamente para esta parte.

---

## Matplotlib — dibujar el tablero y las pantallas

Matplotlib es la librería de dibujo de todo el proyecto: el tablero, el pato, la mira, y las pantallas de reacción.

**Dónde se usa:**

- **El tablero y el grid** (`dibujar_tablero`, `dibujar_tablero_para_ronda`): `ax.imshow(imagen, cmap="gray")` muestra la matriz de píxeles como imagen, y `ax.axhline`/`ax.axvline` dibujan las líneas rojas de la cuadrícula encima.
- **El pato** (`pato()`): `ax.imshow(sprite, extent=[...])` dibuja el sprite del pato como una capa sobre el tablero ya dibujado. Matplotlib compone la transparencia del PNG automáticamente al renderizar, así que no hace falta mezclar los colores a mano.
- **La mira** (`pistola()`): `Rectangle` (de `matplotlib.patches`) dibuja el borde de la celda de impacto, y `ax.plot(..., marker="x")` dibuja la marca en el centro — piezas ya construidas de la librería, en vez de calcular la geometría a mano.
- **Las pantallas de reacción** (`mostrar_pantalla_reaccion`): muestra `ganador.jpeg` o `gameover.jpg` a pantalla completa, sin texto — la imagen del perro ya comunica el resultado.
- **La pantalla final** (`mostrar_pantalla_final`, `dibujar_panel_con_fondo`): `ax.text(...)` dibuja el resumen de la partida sobre `gameover.jpg`, con `path_effects.Stroke` para el contorno negro que lo hace legible sobre la foto. El panel de gráficos de la Sección 9 usa el mismo truco: un eje que ocupa toda la figura muestra la imagen de fondo, y los 4 gráficos se dibujan encima con `ax.set_facecolor((1, 1, 1, 0.88))` — un fondo blanco *semi-transparente* (RGBA) que deja ver la foto detrás sin perder legibilidad.

**Por qué esta y no otra:** es la librería de visualización estándar de Python y la única capaz de mostrar tanto imágenes (`imshow`) como formas vectoriales (`Rectangle`, `plot`, `text`) en el mismo lienzo, que es exactamente lo que necesita el proyecto: superponer sprites, líneas, gráficos y texto sobre una imagen de fondo.

---

## Seaborn — los gráficos estadísticos finales

Seaborn se usa exclusivamente en la Sección 9, para los gráficos de cierre del proyecto. Está construido encima de Matplotlib, pero da gráficos estadísticos con mucho menos código y con un estilo visual más prolijo por defecto.

**Dónde se usa:**

- **Gráfico de barras** (`graficar_barras_resultado`): `sns.barplot(...)` compara la cantidad de aciertos contra fallos.
- **Pie chart** (`graficar_pie_resultado`): en este caso usamos `ax.pie` de Matplotlib directamente, porque Seaborn no tiene una función de pie chart propia — es un ejemplo real de cuándo conviene usar cada librería según lo que hace falta, no usar una por usarla.
- **Heatmap** (`graficar_heatmap_resultado`): `sns.heatmap(total, annot=etiquetas, cmap="Reds")` colorea cada celda del grid según cuántos disparos cayeron ahí, con una etiqueta de texto tipo `"1A / 2F"` (aciertos/fallos) superpuesta en cada casilla — hacer esto mismo a mano con Matplotlib puro pediría mucho más código (normalizar colores, dibujar cada celda, poner cada etiqueta).
- **Histograma** (`graficar_histograma_resultado`): `sns.histplot(data=df, x="disparo_fila", hue="Resultado", multiple="stack", ...)` cuenta cuántos disparos cayeron en cada fila, apilando aciertos y fallos con un color distinto cada uno — la misma idea que el heatmap, pero en una sola dimensión.
- **Leaderboard** (`mostrar_leaderboard`): otro `sns.barplot`, esta vez comparando el % de aciertos de todas las partidas guardadas en el CSV histórico.

**Por qué esta y no otra:** el enunciado la pide explícitamente para "elaboración de gráficos estadísticos finales", y en la práctica ahorra código real en el heatmap y en las barras en comparación con hacerlo todo con Matplotlib puro.

---

## Pillow (PIL) — cargar imágenes desde disco

Pillow es una librería de apoyo (no está en la lista obligatoria del enunciado, pero es necesaria para poder usar NumPy y Matplotlib con imágenes reales).

**Dónde se usa:**

- **Cargar cualquier imagen del proyecto** (`cargar_fondo`, y las llamadas a `Image.open(...)` para el pato, `ganador.jpeg` y `gameover.jpg`): Pillow lee el archivo PNG/JPEG del disco y lo decodifica; `np.array(imagen)` lo convierte inmediatamente en una matriz de NumPy, que es el formato que el resto del proyecto entiende.

**Por qué esta y no otra:** es la librería estándar de Python para abrir y decodificar archivos de imagen — NumPy y Matplotlib no leen archivos de imagen por sí solos, necesitan que algo los convierta primero en una matriz de píxeles.

---

## Resumen rápido

| Librería | Rol en una frase |
|---|---|
| **NumPy** | Todo lo que es matriz, cuadrícula o número aleatorio |
| **pandas** | Todo lo que es tabla, registro o estadística resumida |
| **Matplotlib** | Todo lo que se dibuja en pantalla: tablero, sprites, texto |
| **Seaborn** | Los gráficos estadísticos de cierre (barras, pie, heatmap, histograma) |
| **Pillow** | Puente entre un archivo de imagen en disco y una matriz de NumPy |
