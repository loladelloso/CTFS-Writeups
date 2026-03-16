El sistema mantiene un estado interno de **128 bits `S`**, derivado de AES.  
Para verificar integridad de hardware, el firmware registra valores de la forma:
S ⊕ ROTR(S, k)
para distintos valores de rotación `k`.

Por un error de logging, se filtran varios de estos valores, junto con:

- los `k` correspondientes  
- **dos bits conocidos del estado** (no los encontramos, pero usamos `1` y `0` porque es lo más normal en este tipo de retos)  
- un **ciphertext cifrado usando el estado**

El objetivo es **reconstruir `S` y recuperar el mensaje cifrado**.

![imagen1](https://github.com/user-attachments/assets/7c7cd9fd-a717-4430-a7ef-36e9d1d9d899)

---

## Reconstrucción del estado (`solveRot.py`)

El script `solveRot.py` se encarga de **reconstruir el estado interno secreto `S` de 128 bits** usando la información filtrada por los logs del sistema.

Cada log tiene la forma:
S ⊕ ROTR(S, k)
donde `ROTR` es una **rotación de bits hacia la derecha**.

La idea clave es que estas ecuaciones son **lineales a nivel de bits**, así que pueden modelarse como **restricciones lógicas**.

El script usa **Z3** para:

1. Crear un vector de **128 bits** que representa `S`.
2. Agregar una ecuación por cada par `(k, valor_filtrado)` conocido.
3. Incorporar los **bits ancla del estado** (los bits conocidos que da el challenge) para romper simetrías y asegurar una solución única.

Una vez que el solver encuentra un **modelo consistente**, el script reconstruye `S` completo y lo imprime en **hexadecimal**.

![imagen2](https://github.com/user-attachments/assets/66f81e3e-f9d5-4061-8a84-ded1f5e0248f)

---

## Descifrado del mensaje (`crypt.py`)

Luego el script `crypt.py` toma el **estado interno `S` ya recuperado** y lo usa para descifrar el `ciphertext` provisto por el challenge.

En este caso, el cifrado es simple: el estado actúa directamente como **keystream**, por lo que descifrar consiste en hacer un **XOR** entre el ciphertext y los bytes de `S`.

El script:

1. Convierte el **estado hexadecimal** en bytes.
2. Hace el **XOR byte a byte** con el ciphertext.
3. Muestra el **mensaje descifrado**.

![imagen3](https://github.com/user-attachments/assets/d919b91d-f2df-460d-850e-10de6ff3009f)
