from fastapi import FastAPI, HTTPException
import logging

# Importamos nuestros módulos de extracción y transformación
from .extractor import fetch_products
from .transformer import process_products

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="Automation Case API",
    description="API ETL ligera que extrae, transforma y expone datos de productos.",
    version="1.0.0"
)

@app.get("/api/v1/processed-data", summary="Obtener datos procesados de productos")
def get_processed_data():
    """
    Este endpoint ejecuta el pipeline ETL:
    1. Extrae los datos de la API pública.
    2. Filtra y transforma la información.
    3. Devuelve la estructura final optimizada.
    """
    try:
        logger.info("Iniciando flujo de automatización...")
        
        # 1. Extracción
        raw_data = fetch_products()
        
        # 2. Procesamiento (Transformación y Filtrado)
        processed_data = process_products(raw_data)
        
        logger.info(f"Flujo completado exitosamente. Registros procesados: {len(processed_data)}")
        
        # 3. Exposición
        return {
            "status": "success",
            "message": "Datos procesados correctamente",
            "total_records": len(processed_data),
            "data": processed_data
        }

    except Exception as e:
        logger.error(f"Error en el pipeline de datos: {str(e)}")
        # Manejo de errores claro devolviendo un HTTP 500 
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al procesar la información: {str(e)}"
        )

# Para propósitos de prueba de salud de la API
@app.get("/health", summary="Health check")
def health_check():
    return {"status": "ok", "message": "El servicio está funcionando."}