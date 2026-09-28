---
# yaml-language-server: $schema=schemas\page.schema.json
Object type:
    - Page
Creation date: "2026-09-28T01:04:34Z"
Created by:
    - 'Richard '
Emoji: "\U0001F4DC"
id: bafyreifkyzon2f522eh3ogwg6hs2dneozcpd6l6jal4rx2zsfjvtopea7u
---
# reporte\_dino\_crash\_eda   
# Mision 1:   
| Escanario   <br> |              Variable objetivo (Y)   <br> |                                                                                                                                                                                                                                                                                                                                                                         Variables de entrada (X)   <br> |        Granularidad   <br> |                                                                                                        Tamaño mínimo razonable   <br> |                              Riesgo si el dataset está mal definido   <br> |
|:-----------------|:------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------|:--------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|
|        P1   <br> | muere\_siguiente\_frame<br>BINARIO   <br> |                                    **distancia\_obstáculo** (para saber que tan lejos esta el obstáculo)<br>**distancia\_suelo** (para saber si alcanza a ezquivar el obstáculo)<br>**velocidad** (para el calculo de si alcanza a esquivar el obstáculo)<br>**tipo\_obstáculo** (para saber si es un cactus o un ave)<br>**altura\_obstáculo** (saber la altura del obstáculo para el esquivo)    <br> | un frame cada 16 ms   <br> | 600,000 <br>Se necesita una gran cantidad de estos ya que se generan un aprox de 60 cada segundo. Esos frames, son solo 10 min   <br> |                                                     Mala predicción   <br> |
|        P2   <br> |         puntaje\_final<br>NUMERICO   <br> |                                                                         **distancia\_recorrida** (para saber su distancia)<br>**num\_obstáculos** (el numero de obstaculos que ezquivado)<br>**puntaje\_anterior** (para comparar el puntaje y registrarlo en caso de que sea mayor)<br>**noche\_dia** (si esta el modo de noche y dia)<br>**dificultad** (saber en que dificultad esta jugando)   <br> | Resumen por partida   <br> |                                                                 50<br>Son partidas completas lo cual ya supone bastante tiempo   <br> |                                       mal calculo del puntaje final   <br> |
|        P3   <br> |       tipo\_obstaculo<br>CATEGORIA   <br> |    **distancia\_recorrida** (saber la distancia que ha recorrido para los pajaros)<br>**noche\_dia** (indica si esta avanzando mucho)<br>**dificultad** (Saber que tipo de obstáculo aparecer)**tiempo\_transcurrido** (cuanto tiempo lleva jugando el nivel para saber que spawnear)<br>distancia\_ultimo\_obstáculo (saber que tanta distancia hay entre el ultimo obstáculo y el jugador)<br>   <br> | un frame cada 16 ms   <br> |                                  600,000<br>Son 10 min de juego, los cuales dan los suficientes frames para una muestra grande   <br> |   Obstáculos imposibles de esquivar (5 cactus uno detrás de otros )   <br> |

# Mision 2:   
1. ¿Qué patrón ves en la fila donde **`died=1` (frame 82)?**   
    `dist_obstacle=12`, `jump=0`, `obstacle_type=cactus_small`. Está muy cerca del obstáculo y no salta.   
2. ¿ **`score` es buena variable para predecir muerte en el siguiente frame? ¿Por qué sí o no?**   
    El score sube con el tiempo, pero no te dice si el obstáculo está cerca. Puede estar correlacionado con la velocidad, pero no con la acción inmediata.   
3. **¿Falta alguna columna crítica para P1?**   
    No, esas son las necesarias   
4. ¿ **`died` tal como está definida sirve para P1 o solo describe el final de la partida?**   
    `died=1` solo en el último frame. Para P1 necesitas saber si **en el siguiente frame** morirá, no si ya murió.   
   
   
# Mision 3:   
1. ¿Hay fugas de información (leakage)?    
    1. No hay fujas, ya que no hay datos que sean afectados por el objetivo (como un nuevo récord)   
    2. Ejemplo, un nuevo récord, digamos que tenemos un dato el cual se llama récord, un dato que se mantiene igual en anteriores frames, pero al siguiente frame este se actualiza, aun no llegas a ese puntaje, pero gracias a que cambio ahora sabes que no morirás hasta llegar a dicho puntaje.    
2. ¿Datos i.i.d.?    
    1. No hay IID   
    2. Sesga el resultado al ya saber lo que pasará   
3. ¿Outliers?    
    1. No hay datos que se salgan de sus valores normales   
   
   
# Misión 4   
Debes responder:   
1. **¿El problema P1 está desbalanceado?** Cuantifica.   
    - 50 muertes en ~12,000 frames = **0.42%** de la clase positiva. Extremadamente desbalanceado.   
2. **¿Qué implica para la métrica?**   
    - Accuracy sería engañosa (un modelo que siempre diga "no muere" acierta el 99.58%). Usa **precision, recall, F1, AUC-PR**.   
3. ¿ **`dist_obstacle` parece útil como predictor?**   
    - Sí: las muertes suelen ocurrir con `dist < 20`. Es una señal fuerte.   
4. ¿La distribución de **`score` sugiere regresión simple o necesitas transformación?**   
    - Cola larga hacia la derecha (media 28 > mediana 18). Podrías necesitar transformación logarítmica o un modelo robusto.   
   
   
# Misión 5    
Te dan una tabla guía que debes **completar y comentar**. Luego, para cada escenario (P1, P2, P3), llenar:   
| Escenario   <br> |                                       Tras tu EDA, ¿Qué fila de la guía aplica?   <br> |                                                                                                                                                                                Modelo que propondrías   <br> |                                                                                                                                                                                                                                                                       2 condiciones del dataset que deben cumplirse   <br> |
|:-----------------|:---------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|        P1   <br> |                    Y binaria muy desbalanceada + secuencia de frames por sesión   <br> |    Regresión logística con class\_weight='balanced' como baseline; Random Forest con class\_weight o Gradient Boosting si hay más datos. Si se explota la secuencia: LSTM/GRU con features por frame.   <br> |    1. Suficientes ejemplos positivos de muerte (no solo 50 en 12,000 frames; idealmente >1,000 para que el modelo aprenda patrones de colisión). 2. Variables bien medidas en el frame previo: dist\_obstacle, jump, altura del dino, speed, tipo de obstáculo. Sin esto, el modelo no puede anticipar la colisión.   <br> |
|        P2   <br> |   Y numérica (score final) + relación posiblemente no lineal con speed y tiempo   <br> |               Regresión lineal/Ridge como baseline; Random Forest regresor o Gradient Boosting regresor si la relación es no lineal. Considerar transformación logarítmica si score tiene cola larga.   <br> |                                                   1. Una fila por partida completa con score\_final conocido (no frames sueltos). 2. Variables resumen por partida: duración, speed promedio/máxima, número de obstáculos esquivados, tipo de obstáculos dominantes. Sin resumen por partida, no hay Y consistente.   <br> |
|        P3   <br> |                        Y categórica multiclase + secuencia de frames por sesión   <br> |                                           Logística multinomial como baseline; Random Forest clasificador o XGBoost multiclase. Si importa el orden temporal: LSTM/GRU con ventana de frames previos.   <br> |          1. Balance razonable entre clases (none, cactus\_small, cactus\_large, bird); si bird es solo 11%, considerar class\_weight o remuestreo. 2. Ventana temporal suficiente: al menos varios frames previos al obstáculo para capturar patrones de aparición. Sin contexto temporal, el modelo solo ve ruido.   <br> |

   
# Mision 6   
   
1. Describe un escenario del dino donde un **árbol profundo** parecería buena idea pero el EDA lo desaconsejaría**.**   
    - pocos datos o muchas variables   
2. Describe un escenario donde una **red neuronal** tendría sentido y qué deberías ver en el EDA para justificarla**.**   
    - muchas partidas y patrones temporales complejos    
3. ¿Se podría resolver P1 con **reglas fijas** ( `si dist_obstacle < X y jump=0 entonces muerte`)? Compara con un modelo aprendido: ventajas y límites.   
    - `si dist_obstacle < 20 y jump=0 → muerte`.    
        - Ventajas: simple, interpretable.    
        - Límites: no captura casos con `bird` a media altura, ni lag del jugador, ni velocidad.   
   
   
