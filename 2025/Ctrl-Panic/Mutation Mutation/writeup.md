## Análisis del reto

Al abrir el link se observa la siguiente página, donde no sucede nada al apretar **F12** o hacer **click derecho** para poder inspeccionar.

![imagen5](https://github.com/user-attachments/assets/8cd589ff-837e-4538-ab01-140267aa8b2c)

Para poder inspeccionar fue necesario hacer:

```
Tres puntos → Más herramientas → Herramientas para desarrolladores
```

---

## Análisis del código

El reto presentaba un **script altamente ofuscado** que utilizaba técnicas de **antidebugging**.  
El código incluía:

### Diccionarios de strings

Un **array de cadenas codificadas** utilizado para ocultar el flujo lógico del programa.

### Intervalos y Timeouts

Bucles infinitos que monitoreaban si:

- la **consola estaba abierta**
- el **DOM cambiaba**

En caso de detectar alguna de estas condiciones, el script **reseteaba el flag** a valores falsos como:

```
lactf{nope}
lactf{wrong_one}
```

---

## Congelar el script

Para poder trabajar sin interferencias, el primer paso fue **"congelar" el estado del script** matando todos los procesos en segundo plano.

Esto permitió evitar que los intervalos siguieran ejecutándose y nos devolvió **una flag falsa**.

Al intentar ejecutar funciones obvias como:

```
f()
```

el script también devolvía **flags falsas**.

Esto indicaba que:

- el autor había implementado lógica para **detectar ejecución directa**, o  
- el **flag real estaba fragmentado** dentro del código.

![imagen6](https://github.com/user-attachments/assets/784b936c-e2cd-4f63-b315-4a9d80d48ec2)

---

## Extracción del flag

Se identificó la función de acceso al **diccionario principal de strings**:

```
_0x58c83c
```

En lugar de intentar entender la compleja matemática utilizada para calcular los índices, por ejemplo:

```
-0x3496d * -0x1 ...
```

se optó por una estrategia más directa: **extraer todos los strings almacenados en memoria**.

Para ello se utilizó un **script de fuerza bruta** que recorría el diccionario y mostraba cualquier string que contuviera el prefijo:

```
lactf{
```

Esto permitió localizar rápidamente los posibles candidatos al **flag real**.

![imagen7](https://github.com/user-attachments/assets/2bdbfd3d-d332-4d83-a5f3-c0a75efa8e3f)
