
# Static

## Información

**URL**

https://teams.duckerz.ru/categories/Steganography/43

**Categoria**

Esteganografía

**Descripción**

Stierlitz turned on the TV.

Static started running on the screen.

Stierlitz got indignant and asked him not to run on the TV.

**Recursos**

- static.gif

## Resolución

Para la resolución del desafío se aplicó un enfoque de análisis esteganográfico a nivel de frames, partiendo de la hipótesis de que la información oculta se encontraba distribuida a lo largo de las imágenes que componen el archivo GIF.

**Extracción de frames**

En primer lugar, se procedió a la extracción de todos los frames del archivo GIF proporcionado. Para ello se utilizó la herramienta `convert` de ImageMagick, que permite descomponer un GIF animado en sus imágenes constituyentes:

```bash
$ convert static.gif frame_%03d.png
```

Como resultado de este proceso, se obtuvieron un total de 120 imágenes en formato PNG, numeradas secuencialmente desde `frame_000.png` hasta `frame_119.png`, correspondientes a cada uno de los frames del GIF original.

**Comparación secuencial de imágenes**

Una vez extraídos los frames, se realizó una comparación secuencial entre imágenes consecutivas, con el objetivo de identificar diferencias visuales mínimas que pudieran contener información esteganográfica.

Para ello se utilizó la herramienta `compare` (también perteneciente a ImageMagick), la cual genera una imagen diferencial que resalta los píxeles distintos entre dos imágenes. Conceptualmente, el procedimiento consistió en comparar cada frame con su inmediato sucesor:

```bash
$ compare frame_000.png frame_001.png diff_000_001.png
$ compare frame_001.png frame_002.png diff_001_002.png
...
```

Este proceso se automatizó mediante un script en bash para realizar la comparación de manera global y sistemática:

```bash
for i in $(seq -w 0 118); do
  j=$(printf "%03d" $((10#$i + 1)))
  compare frame_${i}.png frame_${j}.png diff_${i}_${j}.png
done
```

De esta forma, se generó un conjunto de imágenes diferenciales (`diff_XXX_YYY.png`), cada una representando los cambios entre dos frames consecutivos.

**Identificación de la información oculta**

Tras analizar las imágenes resultantes de la comparación, se observó que la información oculta (flag) se hacía visible de manera progresiva en las imágenes diferenciales. En particular, la flag podía reconstruirse visualmente siguiendo la secuencia de imágenes generadas a partir de las comparaciones, comenzando desde la primera comparación hasta la comparación 40 (a partir de aca, las comparaciones repiten la flag).

Este comportamiento confirma el uso de una técnica de esteganografía basada en variaciones sutiles entre frames consecutivos, donde el mensaje no es perceptible en los frames individuales, pero sí emerge claramente al analizar sus diferencias.

## Flag

DUCKERZ{wh1t3_n0153_0f_d00m_4nd_d3sp41r}
