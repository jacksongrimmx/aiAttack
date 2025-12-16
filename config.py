"""
Configuración centralizada de la aplicación
"""
import os
from datetime import timedelta


class Config:
    """Configuración general de la aplicación"""
    
    # Flask
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))  # Heroku asigna el puerto dinámicamente
    
    # INEGI
    INEGI_BASE_URL = "https://www.inegi.org.mx"
    REQUEST_TIMEOUT = 30
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    # Directorios
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # Archivos de salida
    JSON_FILENAME = 'inegi_data.json'
    CSV_FILENAME = 'inegi_data.csv'
    LATEST_JSON = 'inegi_latest.json'
    
    # Scheduler
    SCRAPING_INTERVAL_MINUTES = 5  # Ejecutar cada 5 minutos
    SCHEDULER_TIMEZONE = 'America/Mexico_City'
    
    # Límites de extracción
    MAX_SECTIONS = 15
    MAX_NEWS = 10
    MAX_INDICATORS = 10
    MAX_LINKS = 20
    
    @classmethod
    def init_app(cls):
        """Inicializar directorios necesarios"""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
