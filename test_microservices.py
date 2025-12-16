"""
Script de prueba para arquitectura de microservicios
"""
from services import ScraperService, StorageService, SchedulerService
from config import Config
from datetime import datetime


def test_microservices():
    """Prueba los microservicios individualmente"""
    
    print("="*70)
    print("PRUEBA DE MICROSERVICIOS - INEGI WEB SCRAPER")
    print("="*70)
    
    # Inicializar configuración
    Config.init_app()
    
    # 1. Probar ScraperService
    print(f"\n[{datetime.now()}] 1️⃣  Probando ScraperService...")
    print("-"*70)
    scraper = ScraperService()
    print(f"✓ ScraperService inicializado")
    print(f"  URL Target: {scraper.base_url}")
    print(f"  Timeout: {scraper.timeout}s")
    
    print(f"\nEjecutando scraping...")
    data = scraper.scrape_homepage()
    
    if data.get('status') == 'success':
        print(f"✓ Scraping exitoso")
        print(f"  Título: {data.get('title')}")
        print(f"  Secciones: {len(data.get('main_sections', []))}")
        print(f"  Noticias: {len(data.get('latest_news', []))}")
        print(f"  Indicadores: {len(data.get('featured_indicators', []))}")
        print(f"  Links: {len(data.get('important_links', []))}")
    else:
        print(f"✗ Error en scraping: {data.get('error')}")
        return False
    
    # 2. Probar StorageService
    print(f"\n[{datetime.now()}] 2️⃣  Probando StorageService...")
    print("-"*70)
    storage = StorageService()
    print(f"✓ StorageService inicializado")
    print(f"  Data Directory: {storage.data_dir}")
    
    # Guardar JSON
    print(f"\nGuardando datos en JSON...")
    if storage.save_json(data, 'test_data.json'):
        print(f"✓ JSON guardado correctamente")
    else:
        print(f"✗ Error guardando JSON")
        return False
    
    # Guardar CSV
    print(f"\nGuardando datos en CSV...")
    if storage.save_csv(data, 'test_data.csv'):
        print(f"✓ CSV guardado correctamente")
    else:
        print(f"✗ Error guardando CSV")
        return False
    
    # Cargar JSON
    print(f"\nCargando datos desde JSON...")
    loaded_data = storage.load_json('test_data.json')
    if loaded_data:
        print(f"✓ JSON cargado correctamente")
        print(f"  Timestamp: {loaded_data.get('timestamp')}")
    else:
        print(f"✗ Error cargando JSON")
        return False
    
    # Listar archivos
    print(f"\nListando archivos en data/...")
    files = storage.list_data_files()
    print(f"✓ {len(files)} archivo(s) encontrado(s)")
    for f in files[:5]:  # Mostrar primeros 5
        print(f"  • {f}")
    
    # 3. Probar SchedulerService
    print(f"\n[{datetime.now()}] 3️⃣  Probando SchedulerService...")
    print("-"*70)
    scheduler = SchedulerService(scraper, storage)
    print(f"✓ SchedulerService inicializado")
    
    # Obtener estado
    status = scheduler.get_status()
    print(f"\nEstado del Scheduler:")
    print(f"  Running: {status['is_running']}")
    print(f"  Jobs: {status['jobs_count']}")
    print(f"  Has Cached Data: {status['has_cached_data']}")
    print(f"  Last Update: {status['last_update']}")
    
    # Iniciar scheduler
    print(f"\nIniciando scheduler (intervalo: 1 hora)...")
    scheduler.start(1)
    
    status = scheduler.get_status()
    print(f"✓ Scheduler iniciado")
    print(f"  Running: {status['is_running']}")
    print(f"  Jobs: {status['jobs_count']}")
    
    # Detener scheduler
    print(f"\nDeteniendo scheduler...")
    scheduler.stop()
    print(f"✓ Scheduler detenido")
    
    # 4. Integración completa
    print(f"\n[{datetime.now()}] 4️⃣  Probando integración completa...")
    print("-"*70)
    
    scheduler2 = SchedulerService(scraper, storage)
    scheduler2.start(1)
    
    print(f"Ejecutando tarea programada manualmente...")
    scheduler2.scheduled_scrape()
    
    cached = scheduler2.get_cached_data()
    if cached:
        print(f"✓ Datos en caché disponibles")
        print(f"  Timestamp: {cached.get('timestamp')}")
    
    scheduler2.stop()
    
    # Resumen
    print("\n" + "="*70)
    print("✅ PRUEBA DE MICROSERVICIOS COMPLETADA EXITOSAMENTE")
    print("="*70)
    print(f"\nServicios probados:")
    print(f"  ✓ ScraperService   - Web scraping del INEGI")
    print(f"  ✓ StorageService   - Persistencia en JSON/CSV")
    print(f"  ✓ SchedulerService - Tareas programadas")
    print(f"  ✓ Integración      - Comunicación entre servicios")
    print("\n" + "="*70)
    
    return True


if __name__ == '__main__':
    try:
        success = test_microservices()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
