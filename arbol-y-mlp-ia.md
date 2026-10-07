---
# yaml-language-server: $schema=schemas\page.schema.json
Object type:
    - Page
Creation date: "2026-10-07T13:28:29Z"
Created by:
    - 'Richard '
Emoji: "\U0001F916"
id: bafyreieptflzg3avvydalh6jdqv3zwrm45tw4azllrc4ypxnr4leqb7miy
---
# Arbol y MLP - IA   
## Parte I. Conceptos y definiciones   
- Pregunta 1   
    ¿Qué es un **árbol de decisión** y cuál es su objetivo principal dentro de un problema de clasificación?   
      Es un algoritmo de clasificación de datos, al darle datos estos los va clasificando en ramas, cada rama indicaría una característica clave de los datos para que cuando ingrese un dato este vaya cayendo en dichas ramas si es que dicho dato tiene las características para caer dentro de esa rama, esto se repite hasta llegar al nodo raiz que es cuando ya se le da una clasificación al dato ingresado. Es de entrenamiento supervisado (datos etiquetados).   
- Pregunta 2   
    Explique con sus propias palabras los siguientes elementos de un árbol de decisión:   
    - Nodo raíz.   
        - El nodo donde comienza el recorrido, la entrada de los datos.   
    - Nodo interno.   
        - Nodo que pregunta una característica al dato para poder estrechando la clasificación del dato (pregunta si el animal tiene uñas retractiles o no)   
    - Rama.   
        - La conexión que existe entre los multiples nodo, como si fuese el camino que recorren los datos.   
    - Hoja.   
        - El nodo más profundo del arbol, el que esta al final de la rama, este nodo es que le daría la clasificación al dato (digamos que clasifica al animal si es perro o gato).   
- Pregunta 3   
    ¿Qué es una **red neuronal multicapa** y qué función cumplen las siguientes capas?   
    - Capa de entrada.   
        - Es la recibe los datos   
    - Capa oculta.   
        - La que procesa la información   
    - Capa de salida.   
        - Genera la clasificación o la predicción final.   
- Pregunta 4   
    ¿Qué representan los **pesos** y los **sesgos** dentro de una red neuronal? Explique también por qué sus valores cambian durante el entrenamiento.   
      Los pesos representan que tanto influyen en la decisión que tomara el modelo   
      El sesgo (no lo recuerdo)   
      Sus valores cambian ya que, con cada época que se hace el modelo los ajusta para obtener la mayor precisión posible (pongamos que cada vez que estudias entiendes mejor los temas de la unidad y relacionas mejor los temas con cada uno, es este mismo proceso, pero para los pesos)   
- Pregunta 5   
    ¿Cuál es la principal diferencia entre la forma en que aprende un árbol de decisión y la forma en que aprende una red neuronal multicapa? Explique qué elementos aprende cada modelo.   
      La principal diferencia son las épocas, cuantas veces un modelo necesita repasar los datos para aprender. El arbol de decisión solo necesita una (con esta genera el arbol) y el MLP necesita varias, las que sean suficiente para aprender de los datos y clasificar o predecir.   
   
   
## Parte II. Análisis y aplicación   
- Pregunta 6   
    Una institución bancaria desea desarrollar un sistema que detecte posibles compras fraudulentas.   
    El sistema dispone de información como:   
- Monto de la compra.   
- Hora de la operación.   
- Ciudad donde se realizó.   
- Tipo de establecimiento.   
- Número de compras realizadas durante el día.   
- Historial de compras del cliente.   
   
Analice las ventajas y desventajas de utilizar un **árbol de decisión** y una **red neuronal multicapa**.   
¿Cuál utilizaría y por qué?   
- Pregunta 7   
    Una escuela quiere detectar estudiantes que presentan riesgo de reprobar una materia.   
    Se conocen variables como:   
- Asistencia.   
- Calificaciones.   
- Tareas entregadas.   
- Participación.   
- Número de materias reprobadas anteriormente.   
   
Suponga que un árbol de decisión y una red neuronal obtienen prácticamente la misma precisión.   
¿Qué otros factores tomaría en cuenta para elegir uno de los dos modelos?   
Justifique su respuesta.   
- Pregunta 8   
    Un hospital desarrolla un sistema para determinar qué pacientes necesitan atención prioritaria utilizando:   
- Edad.   
- Temperatura.   
- Presión arterial.   
- Frecuencia cardiaca.   
- Síntomas.   
- Antecedentes médicos.   
   
Una red neuronal obtiene mejores resultados que un árbol de decisión, pero resulta más difícil explicar cómo obtuvo su respuesta.   
¿Considera que la mayor precisión es suficiente para elegir la red neuronal?   
Analice las consecuencias que podría tener esta decisión.   
- Pregunta 9   
    Una empresa de reparto quiere predecir si un pedido llegará tarde considerando:   
- Distancia.   
- Tráfico.   
- Clima.   
- Hora del día.   
- Cantidad de pedidos.   
- Experiencia del repartidor.   
   
Para determinado pedido, el árbol de decisión indica:   
```
Llegará a tiempo


```
mientras que la red neuronal indica:   
```
Probablemente llegará tarde


```
¿Cómo determinaría cuál de los dos modelos está realizando una mejor predicción?   
Explique qué información adicional debería analizar.   
- Pregunta 10   
    Una empresa desarrolla dos sistemas para decidir si una persona puede recibir un crédito.   
    El primer sistema utiliza un **árbol de decisión** y permite explicar claramente por qué una solicitud fue rechazada.   
    El segundo utiliza una **red neuronal multicapa** y obtiene mejores resultados de predicción, pero es más difícil explicar sus decisiones.   
    Si usted fuera responsable del proyecto:   
- ¿Cuál de los dos modelos utilizaría?   
- ¿Qué ventajas tendría su elección?   
- ¿Qué riesgos tendría?   
- ¿Consideraría posible utilizar ambos modelos dentro del mismo sistema?   
   
Justifique ampliamente su respuesta.   
A partir de los ejercicios anteriores, explique brevemente la siguiente afirmación:   
> No existe un algoritmo de Inteligencia Artificial que sea el mejor para todos los problemas.   

Relacione su respuesta con los conceptos de:   
- Precisión.   
- Interpretabilidad.   
- Cantidad de datos.   
- Complejidad del problema.   
- Consecuencias de una decisión incorrecta.   
