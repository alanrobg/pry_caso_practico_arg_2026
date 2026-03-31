# Arquitectura de la Solución de Automatización

Este documento describe la arquitectura, el flujo de datos y las decisiones técnicas detrás de la solución de automatización construida para extraer, procesar y exponer datos.

## 1. Diagrama de la Solución

```
┌─────────────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────┐
│ Fuente de Datos │ -> │  Extractor  │ -> │ Transformador │ -> │   API REST  │ -> │ Cliente  │
│   Externa       │    │ (requests)  │    │ (Python puro) │    │  (FastAPI)  │    │         │
│ (DummyJSON API) │    └─────────────┘    └──────────────┘    └─────────────┘    └─────────┘
└─────────────────┘           │                    │                    │
                              ▼                    ▼                    ▼
                       ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
                       │ Manejo de   │    │ Reglas de    │    │ Endpoints:  │
                       │ Errores     │    │ Negocio      │    │ - /api/v1/  │
                       │ (Timeouts,  │    │ (Filtrado,   │    │   processed │
                       │  HTTP 4xx/5xx)│    │  Cálculos)  │    │   -data     │
                       └─────────────┘    └──────────────┘    │ - /health   │
                                                              └─────────────┘
```

**Flujo de datos simplificado:**
1. **Extract (Extraer):** Cliente HTTP → API externa → Datos crudos
2. **Transform (Transformar):** Datos crudos → Filtrado → Cálculos → Estructura limpia
3. **Load/Expose (Cargar/Exponer):** Datos procesados → Endpoint REST → Cliente

## 2. Arquitectura de Componentes

### Estructura del Proyecto
```
pry_caso_practico_arg_2026/
├── src/                          # Paquete principal de la aplicación
│   ├── __init__.py              # Inicialización del paquete
│   ├── main.py                  # Punto de entrada FastAPI
│   ├── extractor.py             # Módulo de extracción de datos
│   └── transformer.py           # Módulo de transformación de datos
├── docs/                        # Documentación
│   └── architecture.md          # Este documento
├── requirements.txt             # Dependencias Python
└── README.md                    # Guía de instalación y uso
```

### Componentes Técnicos

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| **Lenguaje Base** | Python 3.9+ | Lenguaje principal para toda la lógica de negocio |
| **Framework Web** | FastAPI | API REST moderna, rápida y con validación automática |
| **Servidor ASGI** | Uvicorn | Servidor de alto rendimiento para aplicaciones asíncronas |
| **Cliente HTTP** | Requests | Extracción de datos con manejo robusto de errores |
| **Validación** | Pydantic | Validación de esquemas y serialización de datos |
| **Logging** | logging (built-in) | Trazabilidad y monitoreo de operaciones |

## 3. Flujo de Datos Detallado

### 3.1 Fase de Extracción
```python
# Pseudocódigo del proceso
def extract():
    try:
        response = requests.get("https://dummyjson.com/products", timeout=10)
        response.raise_for_status()
        raw_data = response.json()
        return raw_data.get("products", [])
    except Timeout:
        raise ExtractionError("Timeout en API externa")
    except HTTPError:
        raise ExtractionError("Error HTTP en API externa")
```

**Características:**
- Timeout de 10 segundos para evitar bloqueos
- Validación de códigos HTTP de error
- Extracción específica del campo "products" del JSON
- Logging detallado de operaciones

### 3.2 Fase de Transformación
```python
# Pseudocódigo del proceso
def transform(raw_products):
    processed = []
    for product in raw_products:
        if product.get("stock", 0) <= 0:
            continue  # Filtrar productos sin stock

        # Cálculos de negocio
        original_price = product.get("price", 0.0)
        discount = product.get("discountPercentage", 0.0)
        final_price = original_price * (1 - discount/100)

        # Estructura final
        processed.append({
            "product_id": product.get("id"),
            "name": str(product.get("title", "")).strip(),
            "category": str(product.get("category", "")).capitalize(),
            "stock_available": product.get("stock"),
            "original_price": round(original_price, 2),
            "final_price": round(final_price, 2)
        })
    return processed
```

**Reglas de negocio aplicadas:**
- **Filtrado:** Solo productos con stock > 0
- **Cálculo de precios:** Precio final = precio original × (1 - descuento/100)
- **Normalización:** Capitalización de categorías, redondeo a 2 decimales
- **Limpieza:** Eliminación de espacios en blanco en nombres

### 3.3 Fase de Exposición
- **Endpoint principal:** `GET /api/v1/processed-data`
- **Endpoint de salud:** `GET /health`
- **Formato de respuesta:** JSON estructurado con metadatos
- **Códigos HTTP:** 200 (éxito), 500 (error interno)

## 4. Decisiones Técnicas y Justificación

### 4.1 Elección de Tecnologías
* **Python + FastAPI vs n8n:**
  - Mayor control granular sobre errores complejos
  - Validación estricta de esquemas con Pydantic
  - Facilita integración en pipelines de CI/CD
  - Mejor mantenibilidad a largo plazo

* **Separación de responsabilidades:**
  - `extractor.py`: Lógica de red y manejo de APIs externas
  - `transformer.py`: Lógica pura de negocio (fácil de testear)
  - `main.py`: Enrutamiento y exposición de endpoints

* **Manejo de errores centralizado:**
  - Excepciones HTTP personalizadas (500 para errores internos)
  - Logging estructurado para debugging
  - Respuestas JSON consistentes

### 4.2 Consideraciones de Seguridad
- **Validación de inputs:** Pydantic valida automáticamente todas las entradas
- **Timeouts:** Prevención de ataques de denegación de servicio por espera
- **Manejo de errores:** No se exponen detalles internos en respuestas de error
- **Dependencias:** Versiones pinned en requirements.txt

### 4.3 Rendimiento y Escalabilidad
- **Procesamiento en memoria:** Adecuado para volúmenes pequeños (< 1000 registros)
- **Operaciones síncronas:** Simplicidad vs concurrencia
- **Sin estado:** Cada petición es independiente
- **Ligero:** Pocos dependencies, rápido arranque

## 5. Desarrollo con IA Generativa

Esta arquitectura fue diseñada con la asistencia de **GitHub Copilot**, que contribuyó en:

- **Diseño modular:** Sugerencias para separación de responsabilidades
- **Manejo de errores:** Patrones robustos de try-except
- **Documentación:** Generación automática de docstrings y comentarios
- **Optimizaciones:** Mejoras en lógica de transformación
- **Validación:** Verificación de esquemas y tipos de datos

## 6. Supuestos y Limitaciones

### Supuestos
* La API externa (`dummyjson.com`) mantiene estructura de respuesta consistente
* Volumen de datos cabe en memoria del proceso
* Conexión a internet disponible para extracción
* Requisitos de negocio no cambian frecuentemente

### Limitaciones Actuales
* **Procesamiento síncrono:** No maneja alta concurrencia
* **Sin caché:** Cada petición consulta la API externa
* **Sin persistencia:** Datos no se almacenan localmente
* **Solo lectura:** No soporta operaciones de escritura

## 7. Próximas Mejoras Potenciales

- **Caché:** Implementar Redis para reducir llamadas a API externa
- **Base de datos:** PostgreSQL para persistencia de datos procesados
- **Autenticación:** JWT para endpoints protegidos
- **Monitoreo:** Métricas con Prometheus/Grafana
- **Tests:** Suite completa de pruebas unitarias e integración
- **Contenedores:** Docker para facilitar despliegue
- **CI/CD:** Pipeline automatizado de testing y deployment