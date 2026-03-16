## Análisis del reto

El reto nos presenta una **aplicación web que genera facturas en formato PDF**.

![imagen8](https://github.com/user-attachments/assets/6e2a83e5-4bdf-4656-aca2-cc7433441425)

---

## Revisión del código

Al revisar el código fuente proporcionado (`server.js`), observamos tres componentes importantes:

### Generador de facturas (Express)

El servidor recibe datos del usuario:

- `name`
- `item`
- `cost`
- `datePurchased`

Estos valores se **concatenan directamente dentro de una plantilla HTML**, sin ningún tipo de **sanitización o limpieza**.

Esto significa que **el usuario puede inyectar HTML arbitrario** dentro de la factura.

---

### Motor de generación de PDF (Puppeteer)

La aplicación utiliza **Puppeteer**, que levanta un navegador **Chrome** en el servidor para:

1. Renderizar el HTML generado
2. Convertirlo en un archivo **PDF**

Como Puppeteer utiliza un **navegador real**, cualquier etiqueta HTML válida será interpretada.

---

### Servicio interno de Flag

Según el archivo `docker-compose.yml`, existe un servicio adicional:

```
flag
```

Este servicio corre en:

```
http://flag:8081
```

y **no es accesible desde el exterior**, pero **sí es visible desde otros contenedores dentro de la red de Docker**, incluyendo el servidor que genera las facturas.

![imagen9](https://github.com/user-attachments/assets/5af35535-830a-4b7e-a3a6-9902b4619ca0)

---

## Identificación de la vulnerabilidad

El punto débil se encuentra en la función:

```
generateInvoiceHTML
```

Debido a la ausencia de sanitización, es posible **inyectar etiquetas HTML arbitrarias**.

Como Puppeteer renderiza el HTML en un navegador real, interpretará etiquetas como:

```
<iframe>
<img>
<script>
```

Esto permite forzar al navegador del servidor a realizar **peticiones a recursos internos**, generando un **Server-Side Request Forgery (SSRF)**.

---

## Estrategia de explotación

El objetivo es obligar al navegador del servidor a realizar una petición a la dirección interna:

```
http://flag:8081/flag
```

y que el contenido devuelto sea **renderizado dentro del PDF** que recibimos.

Para lograrlo, utilizamos el campo **Customer Name** para inyectar un elemento HTML que cargue contenido externo.

Payload utilizado:

```html
<iframe src="http://flag:8081/flag" width="500px" height="100px" style="border:none;"></iframe>
```

Cuando Puppeteer renderiza la factura:

1. El navegador del servidor carga el `<iframe>`
2. Se realiza una petición interna a `http://flag:8081/flag`
3. El contenido del endpoint se renderiza dentro de la página
4. Ese contenido queda **incluido dentro del PDF generado**

De esta manera, el **flag aparece directamente en el PDF descargado**.

---

![imagen10](https://github.com/user-attachments/assets/66ee0c6f-e6cb-4872-9075-e9b0dfaf72fa)
