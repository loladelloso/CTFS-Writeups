## Análisis del Problema

El desafío presentaba un **servicio de autenticación basado en un esquema de desafío-respuesta (Challenge-Response)**.  
El objetivo era obtener acceso como el usuario **Administrator**.

El código fuente revelaba tres componentes críticos:

### Derivación de Clave (KDF)

Se utiliza **HKDF** para generar una `navigation_key` a partir de:

- un **secreto**
- un **challenge del cliente**
- un **token del servidor**

### Generación de Ruta (`compute_path`)

Un algoritmo que utiliza **AES en modo ECB** para transformar el challenge inicial en un valor de **8 bytes** llamado:

```
expected_path
```

### Verificación Vulnerable (`verify_credential`)

Una función de verificación que utiliza un **XOR acumulativo** entre:

- el valor esperado
- la respuesta del usuario
- una máscara HMAC

---

## Identificación de Vulnerabilidades

### A. Hardcoded Secret (Insecure Storage)

En el diccionario `backpack`, el secreto del administrador estaba representado como:

```python
"Administrator": "****************************************************************"
```

Aunque en muchos casos esto es un **placeholder**, el nombre del reto y la lógica sugerían que el secreto real eran literalmente **64 caracteres de asterisco**.

Al probar este valor como `master_key` en **HKDF**, la derivación de la clave fue exitosa.

---

### B. Manipulación Algorítmica (XOR Checksum)

La vulnerabilidad técnica más profunda reside en cómo se valida la identidad.  
El servidor **no compara hashes directamente**, sino que calcula un checksum:

```
checksum = expected ⊕ provided ⊕ mask
```

Para que la autenticación sea exitosa:

```
checksum = 0
```

Esto permite a un atacante despejar el valor necesario de `provided` (la respuesta enviada al servidor):

```
provided = expected ⊕ mask
```

---

## Estrategia de Resolución (Exploit)

Para resolver el reto se desarrolló un **script en Python** que realiza los siguientes pasos.

### 1. Intercepción

Conectarse al servidor y solicitar un inicio de sesión para `Administrator`, enviando un challenge arbitrario, por ejemplo:

```
1122334455667788
```

---

### 2. Simulación Local

Replicar localmente la lógica criptográfica del servidor.

- Utilizar el `server_token` proporcionado por el servidor en tiempo real.
- Replicar la función **HKDF** usando como secreto:

```python
b"*" * 64
```

También se probaron previamente:

```python
"0" * 64
b"\x00" * 64
```

porque el nombre del reto es **Dor4_Null5**.

Luego:

- Ejecutar la función `compute_path` (**AES-ECB**) para obtener el valor `expected`.

---

### 3. Cálculo del HMAC

Generar la máscara `mask` usando:

- la `navigation_key` derivada
- el valor `expected`

---

### 4. Inyección

Calcular el XOR final entre `expected` y `mask` para generar la respuesta perfecta que **anula el checksum del servidor**:

```
provided = expected ⊕ mask
```

Esta respuesta se envía al servidor y permite autenticarse como **Administrator**.

---

![imagen4](https://github.com/user-attachments/assets/f2b1f912-7a21-436f-aaed-d1493b402377)

