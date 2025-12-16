"""
INEGI Web Scraper - Aplicación Principal
Arquitectura de Microservicios con Cron Job cada 5 minutos
"""
from flask import Flask
from flask_cors import CORS
from datetime import datetime

# Importar configuración y servicios
from config import Config
from services import ScraperService, StorageService, SchedulerService
from api import create_routes

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)

# Inicializar microservicios
print("="*60)
print("INEGI WEB SCRAPER - MICROSERVICES ARCHITECTURE")
print("="*60)
print(f"[{datetime.now()}] Inicializando microservicios...")

scraper_service = ScraperService()
print(f"✓ ScraperService inicializado - Target: {Config.INEGI_BASE_URL}")

storage_service = StorageService()
print(f"✓ StorageService inicializado - Data Dir: {Config.DATA_DIR}")

scheduler_service = SchedulerService(scraper_service, storage_service)
print(f"✓ SchedulerService inicializado")

# Registrar rutas de la API
create_routes(app, scraper_service, storage_service, scheduler_service)
print(f"✓ API Routes registradas")
print("="*60)


if __name__ == '__main__':
    print(f"\n[{datetime.now()}] Iniciando servicios...")
    
    # Iniciar scheduler configurado para ejecutar cada 5 minutos
    scheduler_service.start(Config.SCRAPING_INTERVAL_MINUTES)
    
    # Ejecutar scraping inicial
    print(f"\n[{datetime.now()}] Ejecutando scraping inicial...")
    scheduler_service.scheduled_scrape()
    
    print("\n" + "="*60)
    print("🚀 API REST DISPONIBLE - Cron Job cada 5 minutos")
    print("="*60)
    print(f"URL Base: http://localhost:{Config.PORT}")
    print(f"\nEndpoints principales:")
    print(f"  • GET  /                    - Información de la API")
    print(f"  • GET  /api/scrape          - Ejecutar scraping")
    print(f"  • GET  /api/data            - Obtener datos")
    print(f"  • GET  /api/status          - Estado del sistema")
    print(f"  • GET  /api/files           - Listar archivos")
    print(f"  • POST /api/schedule        - Configurar intervalo")
    print("="*60)
    print(f"⏰ Scraping automático cada {Config.SCRAPING_INTERVAL_MINUTES} minutos")
    print("="*60)
    
    try:
        app.run(
            debug=Config.DEBUG,
            host=Config.HOST,
            port=Config.PORT,
            use_reloader=False
        )
    except (KeyboardInterrupt, SystemExit):
        print(f"\n[{datetime.now()}] Deteniendo servicios...")
        scheduler_service.stop()
        print(f"[{datetime.now()}] Aplicación cerrada correctamente")
