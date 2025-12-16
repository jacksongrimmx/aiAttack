"""
Script de prueba para verificar el Cron Job cada 5 minutos
"""
import time
from datetime import datetime
from config import Config
from services import ScraperService, StorageService, SchedulerService

print("="*70)
print("PRUEBA DE CRON JOB - SCRAPING CADA 5 MINUTOS")
print("="*70)

# Inicializar servicios
scraper_service = ScraperService()
storage_service = StorageService()
scheduler_service = SchedulerService(scraper_service, storage_service)

print(f"\n✓ Servicios inicializados")
print(f"  Intervalo configurado: {Config.SCRAPING_INTERVAL_MINUTES} minutos")

# Iniciar scheduler
print(f"\n[{datetime.now()}] Iniciando scheduler...")
scheduler_service.start(Config.SCRAPING_INTERVAL_MINUTES)

# Ejecutar primer scraping
print(f"\n[{datetime.now()}] Ejecutando primer scraping...")
scheduler_service.scheduled_scrape()

print("\n" + "="*70)
print("⏰ CRON JOB ACTIVO - El scraping se ejecutará automáticamente")
print(f"   Próxima ejecución en {Config.SCRAPING_INTERVAL_MINUTES} minutos")
print("="*70)
print("\nPresiona Ctrl+C para detener...")
print("\nEsperando ejecuciones automáticas:")
print("-"*70)

# Mantener el script corriendo para ver las ejecuciones automáticas
try:
    execution_count = 1
    while True:
        time.sleep(60)  # Esperar 1 minuto
        minutes_passed = execution_count
        next_run_in = Config.SCRAPING_INTERVAL_MINUTES - (minutes_passed % Config.SCRAPING_INTERVAL_MINUTES)
        
        print(f"[{datetime.now()}] ⏱️  {minutes_passed} minuto(s) transcurrido(s) - Próxima ejecución en {next_run_in} minuto(s)")
        execution_count += 1
        
except KeyboardInterrupt:
    print(f"\n\n[{datetime.now()}] Deteniendo scheduler...")
    scheduler_service.stop()
    print(f"[{datetime.now()}] Prueba finalizada correctamente")
    print("="*70)
