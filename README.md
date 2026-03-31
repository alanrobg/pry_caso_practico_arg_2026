# Caso Técnico - Automation Developer: Pipeline ETL con Python

## Descripción de la solución
[cite_start]Esta solución implementa un pipeline de automatización estructurado bajo el patrón ETL (Extract, Transform, Load/Expose)[cite: 76]. [cite_start]Su objetivo es consumir información desde una fuente de datos externa, limpiar y transformar dicha información aplicando reglas de negocio, y finalmente exponer el resultado de forma estructurada a través de un endpoint REST[cite: 29, 31, 35].

## Tecnologías usadas
[cite_start]Para esta implementación se optó por un stack basado enteramente en código[cite: 77]:
* [cite_start]**Python 3.9+**: Lenguaje principal utilizado para la lógica de extracción y transformación de datos[cite: 45].
* [cite_start]**FastAPI**: Framework web moderno y de alto rendimiento elegido para construir y exponer la API[cite: 37].
* **Requests**: Librería utilizada para la extracción de datos HTTP, implementando manejo de timeouts y errores de conexión.
* **Uvicorn**: Servidor ASGI local para ejecutar la aplicación.

## Decisiones tomadas
* [cite_start]**Enfoque basado en código (Python) vs No-Code (n8n):** Se decidió utilizar Python puro y FastAPI en lugar de herramientas visuales para garantizar un control granular sobre el manejo de errores, facilitar la validación estricta de datos y permitir una arquitectura altamente modular y mantenible[cite: 8, 79].
* **Separación de responsabilidades:** El código está dividido en módulos (`extractor.py`, `transformer.py` y `main.py`) para aislar la lógica de red de la lógica de negocio.
* [cite_start]**Manejo de errores centralizado:** Se implementaron bloques `try-except` que capturan fallos de la API externa o de procesamiento interno, devolviendo códigos HTTP claros (ej. 500) y mensajes en formato JSON para evitar caídas silenciosas del servicio[cite: 60, 62, 63, 64].

[cite_start]*Nota: La documentación detallada sobre el flujo de datos y el diagrama de la solución se encuentra en `/docs/architecture.md`*[cite: 66, 68].

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

