import requests
import logging

# Configuración básica de logs para trazabilidad
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_products(api_url: str = "https://dummyjson.com/products") -> list:
    """
    Obtiene la lista de productos desde la API pública especificada.
    """
    try:
        logger.info(f"Iniciando extracción de datos desde: {api_url}")
        
        # Hacemos la petición con un timeout de 10 segundos para evitar que el proceso se quede colgado
        response = requests.get(api_url, timeout=10)
        
        # Esto lanzará una excepción automáticamente si el código HTTP es un error (ej. 404, 500)
        response.raise_for_status() 
        
        data = response.json()
        
        # DummyJSON devuelve los productos dentro de la llave 'products'
        logger.info("Extracción exitosa.")
        return data.get("products", [])
        
    except requests.exceptions.Timeout:
        logger.error("Timeout: La API externa tardó demasiado en responder.")
        raise Exception("Error de conexión: Timeout al contactar la fuente de datos.")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error HTTP al extraer datos: {e}")
        raise Exception(f"Error de extracción de la API: {str(e)}")