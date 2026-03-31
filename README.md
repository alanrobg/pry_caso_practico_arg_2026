# Caso Técnico - Automation Developer: Pipeline ETL con Python

## Descripción de la solución
Esta solución implementa un pipeline de automatización estructurado bajo el patrón ETL (Extract, Transform, Load/Expose). Su objetivo es consumir información desde una fuente de datos externa, limpiar y transformar dicha información aplicando reglas de negocio, y finalmente exponer el resultado de forma estructurada a través de un endpoint REST.

## Tecnologías usadas
Para esta implementación se optó por un stack basado enteramente en código:
* **Python 3.9+**: Lenguaje principal utilizado para la lógica de extracción y transformación de datos.
* **FastAPI**: Framework web moderno y de alto rendimiento elegido para construir y exponer la API.
* **Requests**: Librería utilizada para la extracción de datos HTTP, implementando manejo de timeouts y errores de conexión.
* **Uvicorn**: Servidor ASGI local para ejecutar la aplicación.

## Decisiones tomadas
* **Enfoque basado en código (Python) vs No-Code (n8n):** Se decidió utilizar Python puro y FastAPI en lugar de herramientas visuales para garantizar un control granular sobre el manejo de errores, facilitar la validación estricta de datos y permitir una arquitectura altamente modular y mantenible.
* **Separación de responsabilidades:** El código está dividido en módulos (`extractor.py`, `transformer.py` y `main.py`) para aislar la lógica de red de la lógica de negocio.
* **Manejo de errores centralizado:** Se implementaron bloques `try-except` que capturan fallos de la API externa o de procesamiento interno, devolviendo códigos HTTP claros (ej. 500) y mensajes en formato JSON para evitar caídas silenciosas del servicio.

*Nota: La documentación detallada sobre el flujo de datos y el diagrama de la solución se encuentra en `/docs/architecture.md`*.

## Cómo ejecutar o probar

**1. Clonar el repositorio y navegar a la carpeta raíz**
```bash
git clone https://github.com/alanrobg/pry_caso_practico_arg_2026.git
cd automation-case/src

**2.Crear y activar un entorno virtual**
python -m venv venv

# En Linux o macOS:
source venv/bin/activate  

# En Windows:
venv\Scripts\activate

**3. Instalar las dependencias**
pip install fastapi uvicorn requests

**4. Ejecutar el servidor local**
uvicorn main:app --reload

Ejemplos de uso (Request / Response)
Puedes probar el endpoint principal realizando una petición GET mediante cURL, Postman o desde el mismo navegador:

curl -X 'GET' 'http://localhost:8000/api/v1/processed-data' -H 'accept: application/json'

