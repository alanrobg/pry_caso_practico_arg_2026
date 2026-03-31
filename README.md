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

## Desarrollo con IA Generativa

Esta solución fue desarrollada integrando herramientas de Inteligencia Artificial generativa al entorno de desarrollo:

* **GitHub Copilot:** Se utilizó como asistente de programación principal para:
  - Generar código base y estructuras iniciales
  - Sugerir mejoras en el manejo de errores y validaciones
  - Optimizar la lógica de transformación de datos
  - Documentar funciones y endpoints de manera automática
  - Resolver problemas de importación y configuración de módulos

La integración de IA permitió acelerar el desarrollo, mejorar la calidad del código y mantener mejores prácticas de programación a lo largo del proyecto.

*Nota: La documentación detallada sobre el flujo de datos y el diagrama de la solución se encuentra en `/docs/architecture.md`*.

## Estructura del Proyecto
```
pry_caso_practico_arg_2026/
├── src/
│   ├── __init__.py         # Paquete Python
│   ├── main.py             # Punto de entrada y definición del endpoint (FastAPI)
│   ├── extractor.py        # Lógica para conectarse a la API externa y manejar errores
│   └── transformer.py      # Lógica pura de filtrado y transformación de datos
├── docs/
│   └── architecture.md     # Documentación de flujo de datos y decisiones técnicas
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Instrucciones de ejecución y documentación principal
```

## Cómo ejecutar o probar

**1. Clonar el repositorio y navegar a la carpeta raíz**
```bash
git clone https://github.com/alanrobg/pry_caso_practico_arg_2026.git
cd pry_caso_practico_arg_2026
```

**2. Crear y activar un entorno virtual**
```bash
python -m venv venv

# En Linux o macOS:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

**3. Instalar las dependencias**
```bash
pip install -r requirements.txt
```

**4. Ejecutar el servidor local**
```bash
uvicorn src.main:app --reload
```

El servidor se iniciará en `http://localhost:8000`.

## Endpoints disponibles

- **GET /api/v1/processed-data**: Ejecuta el pipeline ETL completo y devuelve los datos procesados.
- **GET /health**: Verifica el estado del servicio.

## Ejemplos de uso (Request / Response)

Puedes probar los endpoints realizando peticiones GET mediante cURL, Postman o desde el navegador:

```bash
# Endpoint principal
curl -X 'GET' 'http://localhost:8000/api/v1/processed-data' -H 'accept: application/json'

# Health check
curl -X 'GET' 'http://localhost:8000/health' -H 'accept: application/json'
```

### Respuesta de ejemplo del endpoint principal:
```json
{
  "status": "success",
  "message": "Datos procesados correctamente",
  "total_records": 30,
  "data": [
    {
      "product_id": 1,
      "name": "Essence Mascara Lash Princess",
      "category": "Beauty",
      "stock_available": 99,
      "original_price": 9.99,
      "final_price": 8.94
    }
  ]
}
```

