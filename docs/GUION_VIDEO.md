# Guion para el video — Simulación Duck Hunt

Guion pensado para leerse casi textual mientras grabás pantalla, corriendo `DuckHunt_Simulacion.ipynb` de arriba hacia abajo. Las líneas entre `[corchetes]` son indicaciones de qué hacer en pantalla, no se leen en voz alta.

Duración aproximada si lo leés a ritmo normal: **8-10 minutos**.

---

## 0. Introducción (30-40 segundos)

[Mostrar el notebook cerrado / la portada, sin correr nada todavía]

> "Hola, en este video voy a explicar el proyecto de curso de Programación 101: una simulación del videojuego Duck Hunt hecha en Python. El objetivo del proyecto es aplicar programación estructurada, funciones, números aleatorios, manipulación de matrices e imágenes, y estadística básica, usando cuatro librerías obligatorias: NumPy, pandas, Matplotlib y Seaborn.
>
> El programa simula que aparece un pato en una celda al azar de una cuadrícula, se dispara a otra celda al azar, y se valida si coinciden. Esto se repite un número configurable de veces, y al final se muestran estadísticas de toda la partida.
>
> Voy a recorrer el notebook de arriba hacia abajo, sección por sección, mostrando el código y ejecutándolo en vivo."

---

## 1. Configuración inicial y constantes

[Ejecutar la celda de imports (Sección 1)]

> "Esta primera celda importa las cuatro librerías obligatorias: NumPy para matrices y aleatoriedad, pandas para el registro de disparos, Matplotlib para dibujar el tablero, y Seaborn para los gráficos finales. También importamos Pillow para cargar imágenes, y `Rectangle` de Matplotlib, que vamos a usar más adelante para la mira.
>
> Después definimos las rutas a los archivos de la carpeta `assets`: el fondo, el sprite del pato, y las dos imágenes de reacción, ganador y game over.
>
> La función `verificar_assets()` revisa que esos cuatro archivos existan antes de seguir — si falta alguno, el programa se detiene ahí mismo con un mensaje claro, en vez de fallar más adelante con un error confuso. Esto es una buena práctica: validar temprano."

[Mostrar el mensaje "✅ Todos los recursos gráficos fueron encontrados correctamente."]

---

## 2. Configuración de la partida

[Ejecutar la celda de configuración (Sección 2)]

> "Acá están las tres variables que configuran la partida: el nombre del jugador, el número de disparos, y el tamaño del grid. El enunciado pide explícitamente que el número de disparos sea configurable desde el código — por defecto es 20, pero se puede cambiar a 30, 40, o cualquier valor entre 5 y 99 simplemente editando esta línea."

[Opcional — demostrar la validación: cambiar `NUM_DISPAROS = 200` y volver a correr la celda para mostrar el `ValueError`, después volver a dejarlo en un valor válido y re-ejecutar]

> "Si pongo un valor fuera de rango, `validar_configuracion()` lo detecta y lanza un error explicando exactamente qué está mal, en vez de dejar que el problema aparezca más adelante en otra celda que no tiene nada que ver con la configuración."

---

## 3. Carga y preprocesamiento del fondo

[Mostrar la celda markdown con la fórmula de escala de grises]

> "Una imagen a color es una matriz de tres dimensiones: alto, ancho, y tres canales de color, rojo, verde y azul. Para convertirla a escala de grises usamos la fórmula de luminosidad, que le da más peso al verde porque el ojo humano es más sensible a ese color: 0.299 por rojo, más 0.587 por verde, más 0.114 por azul. Con NumPy esto se calcula para toda la imagen de una sola vez, sin recorrer píxel por píxel con un bucle.
>
> El enunciado pide mostrar el fondo en blanco y negro o escala de grises, así que todo el proyecto trabaja únicamente en escala de grises — no se usa color en ningún lado del juego."

[Ejecutar las celdas de funciones, y la celda de orquestación que muestra el fondo en escala de grises]

> "Acá se ve el fondo ya convertido a escala de grises, dividido en la cuadrícula de 4 por 4 configurada antes. Los números amarillos son las coordenadas fila-columna de cada celda."

---

## 4. Función `pato()`

[Mostrar la celda markdown de la Sección 4]

> "`pato()` tiene que hacer dos cosas: elegir una celda al azar usando NumPy, y dibujar el sprite del pato en esa celda.
>
> Para dibujar el sprite usamos `imshow` de Matplotlib con un parámetro `extent`, que le dice en qué rectángulo del tablero pintar la imagen. Lo importante acá es que Matplotlib ya compone la transparencia del PNG automáticamente al dibujarlo — no hace falta escribir una fórmula para mezclar los píxeles a mano, solo hay que decirle dónde dibujarlo.
>
> Para que eso funcione, el sprite necesita tener transparencia real. El archivo original del pato no la tenía — tenía un fondo celeste sólido pintado como parte de la imagen. Eso se solucionó una sola vez, de antemano: preparamos una versión limpia del sprite quitando ese fondo con una técnica llamada chroma-key, la misma idea de una pantalla verde de televisión, y la guardamos como un archivo aparte, `pato_limpio.png`. El notebook ya carga directamente esa versión limpia, así el código de `pato()` se mantiene simple y enfocado en lo que tiene que hacer: elegir la celda y dibujar."

[Ejecutar las celdas de la Sección 4, mostrar la prueba de `pato()`]

> "Acá se ve el resultado: el pato aparece en una celda distinta cada vez que corremos la función, siempre elegida al azar con NumPy."

---

## 5. Función `pistola()`

[Mostrar la celda markdown de la Sección 5]

> "`pistola()` también elige una celda al azar, reutilizando la misma función `generar_posicion_aleatoria()` que ya usa `pato()`. Para marcar la celda de impacto usamos dos piezas que Matplotlib ya trae hechas: un `Rectangle` para dibujar el borde de la celda completa, y un marcador `x` para el centro. No hace falta calcular una figura geométrica a mano — es aprovechar herramientas que la librería ya ofrece."

[Ejecutar la celda, mostrar la prueba de `pistola()`]

> "Acá se ve la mira marcando la celda del disparo: el rectángulo rojo alrededor de toda la celda, y la equis en el centro."

---

## 6. Validación de impacto (WINNER / GAME OVER)

[Mostrar la celda markdown de la Sección 6]

> "Ahora comparamos la posición del pato contra la del disparo. En Python, comparar dos tuplas con el operador `==` compara automáticamente cada elemento — fila con fila, columna con columna — así que no hace falta escribir esa comparación a mano.
>
> `procesar_disparo()` hace esa validación y arma un diccionario con los datos del disparo: en qué celda apareció el pato, en qué celda cayó el disparo, y si hubo acierto o no. Ese diccionario es lo que después se junta en una tabla para las estadísticas.
>
> Si hay coincidencia, se muestra la pantalla `ganador.jpeg` con el texto WINNER en verde; si no, se muestra `gameover.jpg` con el texto GAME OVER en rojo. El texto se dibuja con un contorno negro alrededor, para que se lea bien sobre cualquier fondo de la imagen."

[Ejecutar la celda, mostrar primero la pantalla WINNER forzada, después la pantalla GAME OVER forzada]

> "Estas dos pruebas fuerzan un acierto y un fallo a propósito, para mostrar las dos pantallas de reacción sin depender del azar."

---

## 7. Bucle principal del juego

[Mostrar la celda markdown de la Sección 7]

> "Acá se junta todo: el bucle principal repite pato, pistola, y procesar disparo, exactamente la cantidad de veces configurada en la Sección 2 — y esto es importante: el juego **no se corta** en el primer fallo, siempre se juegan todos los disparos configurados, porque para las estadísticas finales hace falta la mayor cantidad de datos posible.
>
> Cada ronda abre un solo tablero, dibuja el pato y la mira juntos en la misma imagen, y después muestra la pantalla de reacción a pantalla completa."

[Ejecutar la celda del bucle principal — dejar correr unas 3 o 4 rondas mostrando pantalla completa, y después indicar que se puede acelerar o cortar el video para no mostrar las 20 rondas completas]

> "Voy a dejar correr un par de rondas para que se vea el flujo completo... [mostrar 2-3 rondas] ...y ahora avanzo el video para no mostrar las veinte rondas completas — el patrón es siempre el mismo."

[Mostrar el mensaje final: "Partida terminada: 20 disparos registrados para JUGADOR."]

---

## 8. Pantalla final, estadísticas y registro en CSV

[Mostrar la celda markdown de la Sección 8]

> "Con la lista de resultados de los veinte disparos armamos una tabla de pandas, calculamos el resumen — total de disparos, aciertos, fallos, porcentaje de aciertos y porcentaje de fallos — y mostramos una pantalla final reutilizando la imagen de game over, esta vez con el resumen de la partida superpuesto, para distinguirla de la reacción de fallo de cada disparo individual.
>
> Por último, guardamos una fila en un archivo CSV histórico. Como se abre en modo 'agregar', cada partida que se juega se suma a las anteriores sin borrarlas — así se arma un historial de todos los jugadores que prueben el notebook."

[Ejecutar la celda, mostrar la tabla de los 20 disparos, el resumen, y la pantalla final]

---

## 9. Visualización estadística final

[Mostrar la celda markdown de la Sección 9]

> "Para cerrar, generamos gráficos estadísticos usando pandas, Matplotlib y Seaborn: un gráfico de barras comparando aciertos contra fallos, un pie chart con la proporción de aciertos, y un heatmap mostrando en qué celdas del grid apareció el pato con más frecuencia — reutilizando la misma matriz de conteo por celda que ya usamos para el grid."

[Ejecutar la celda, mostrar el panel de 3 gráficos]

> "Y para terminar, un leaderboard: la tabla de todas las partidas guardadas en el CSV histórico, ordenadas por porcentaje de aciertos, con un gráfico de barras comparando a todos los jugadores que hayan probado el notebook."

[Ejecutar la última celda, mostrar la tabla y el gráfico de leaderboard]

---

## Cierre (20-30 segundos)

> "Resumiendo: el proyecto cumple con las cuatro librerías obligatorias — NumPy para las matrices, la aleatoriedad y las conversiones de imagen; pandas para el registro y las estadísticas; Matplotlib para todo el dibujo del tablero y las pantallas; y Seaborn para los gráficos finales. El código está dividido en funciones pequeñas, cada una con una responsabilidad clara, y con comentarios explicando el porqué de cada decisión, no solo el qué.
>
> Eso es todo, gracias por ver el video."

---

## Notas para grabar (no leer en voz alta)

- Si algo sale distinto en pantalla porque el pato/disparo son aleatorios, no importa — la explicación sigue siendo válida, solo cambian las celdas exactas.
- Si querés acortar el video, la Sección 7 (bucle principal) es la más larga de mostrar en vivo — está bien cortar a los primeros 2-3 disparos y saltar directo al mensaje final.
- Antes de grabar, corré todo el notebook una vez de punta a punta (`Kernel → Restart & Run All` o equivalente) para confirmar que no hay errores y que `registros_jugadores.csv` va a tener al menos una fila para el leaderboard de la Sección 9.
- Si el equipo también quiere mostrar el modo jugable (`juego_jugable/`, con pygame), es un buen cierre adicional: "además armamos una versión jugable de verdad, con clic del mouse y colisión por celda, como bonus fuera de lo pedido en el enunciado" — pero no es necesario para cumplir la consigna.
