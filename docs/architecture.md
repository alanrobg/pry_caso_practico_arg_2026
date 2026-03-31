# Arquitectura de la Solución de Automatización

Este documento describe la arquitectura, el flujo de datos y las decisiones técnicas detrás de la solución de automatización construida para extraer, procesar y exponer datos.

## 1. Diagrama de la Solución

El siguiente es un diagrama simple del flujo de la aplicación:

[ Fuente de Datos Externa ] ---> ( Extractor ) ---> ( Transformador ) ---> ( Endpoint API ) ---> [ Cliente ]
     (DummyJSON API)               (requests)           (Python puro)          (FastAPI)

## 2. Componentes Usados

La solución se construyó utilizando un enfoque de microservicio ligero con los siguientes componentes:
* **Python 3:** Lenguaje principal por su versatilidad en el manejo y transformación de datos.
* **FastAPI:** Framework web moderno y rápido para exponer el resultado mediante un endpoint REST.
* **Uvicorn:** Servidor ASGI para ejecutar la aplicación FastAPI.
* **Requests / httpx:** Cliente HTTP para la extracción de datos desde la API pública.
* **Pydantic:** Utilizado (integrado en FastAPI) para la validación de inputs y estructuración de las respuestas.

## 3. Flujo de Datos

El pipeline sigue un enfoque ETL (Extract, Transform, Load/Expose) simplificado:
1. **Extracción:** Un cliente HTTP realiza una petición GET a `dummyjson.com` para obtener un listado crudo de productos o usuarios. Se implementa manejo de errores para capturar fallos de red o timeouts.
2. **Procesamiento:** * **Filtrado:** Se descartan los registros que no cumplen con las reglas de negocio (ej. productos sin stock).
   * **Transformación:** Se estandarizan los formatos de los campos y se calculan nuevos valores (ej. precio con descuento aplicado).
   * **Estructuración:** Se genera una nueva estructura de datos (JSON) optimizada para el cliente final.
3. **Exposición:** El dato procesado se expone a través de un endpoint `GET /api/v1/processed-data` servido por FastAPI.

## 4. Decisiones Técnicas

* **Uso de Python + FastAPI en lugar de n8n:** Aunque n8n es excelente para flujos visuales, una solución basada en código con Python y FastAPI ofrece mayor control sobre el manejo de errores complejos, la validación estricta de esquemas (Pydantic) y facilita la integración en procesos de CI/CD.
* **Separación de responsabilidades:** La lógica de extracción, la de transformación y la del enrutamiento (API) están en módulos separados. Esto mejora la mantenibilidad de la solución a largo plazo y facilita la creación de pruebas unitarias.
* **Manejo centralizado de errores:** Se decidió envolver las llamadas externas en bloques `try-except` que lanzan excepciones HTTP personalizadas para devolver respuestas claras (ej. HTTP 502 si la API externa falla), evitando que el servicio se caiga inesperadamente.

## 5. Supuestos

* Se asume que la API pública (`dummyjson.com`) tiene una estructura de respuesta consistente, aunque se incluyó tolerancia a fallos en caso de indisponibilidad.
* Se asume que el volumen de datos extraído por petición cabe en la memoria de la aplicación (procesamiento en memoria sin necesidad de almacenamiento intermedio o base de datos).
* El endpoint de exposición es de solo lectura (GET) para esta iteración.