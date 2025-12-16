"""
Servicio de Programación - Microservicio para tareas programadas
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from config import Config


class SchedulerService:
    """Servicio especializado en programación de tareas automáticas"""
    
    def __init__(self, scraper_service, storage_service):
        """
        Inicializa el servicio de programación
        
        Args:
            scraper_service: Instancia del servicio de scraping
            storage_service: Instancia del servicio de almacenamiento
        """
        self.scraper_service = scraper_service
        self.storage_service = storage_service
        self.scheduler = BackgroundScheduler()
        self.cached_data = {}
        self.is_running = False
    
    def start(self, interval_minutes=None):
        """
        Inicia el scheduler con tareas programadas
        
        Args:
            interval_minutes (int): Intervalo en minutos entre scraping
        """
        if self.is_running:
            print(f"[{datetime.now()}] [SchedulerService] Scheduler ya está ejecutándose")
            return
        
        if interval_minutes is None:
            interval_minutes = Config.SCRAPING_INTERVAL_MINUTES
        
        # Agregar tarea programada
        self.scheduler.add_job(
            self.scheduled_scrape,
            'interval',
            minutes=interval_minutes,
            id='scrape_job',
            name='INEGI Scheduled Scraping'
        )
        
        self.scheduler.start()
        self.is_running = True
        
        print(f"[{datetime.now()}] [SchedulerService] Scheduler iniciado")
        print(f"  - Intervalo: cada {interval_minutes} minuto(s)")
    
    def stop(self):
        """Detiene el scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            print(f"[{datetime.now()}] [SchedulerService] Scheduler detenido")
    
    def scheduled_scrape(self):
        """Tarea programada para ejecutar scraping"""
        print(f"[{datetime.now()}] [SchedulerService] Ejecutando scraping programado...")
        
        try:
            # Ejecutar scraping
            data = self.scraper_service.scrape_homepage()
            
            # Guardar en caché
            self.cached_data = data
            
            # Persistir datos
            self.storage_service.save_json(data, Config.LATEST_JSON)
            self.storage_service.save_json(data, Config.JSON_FILENAME)
            self.storage_service.save_csv(data, Config.CSV_FILENAME)
            
            print(f"[{datetime.now()}] [SchedulerService] Scraping programado completado")
            
        except Exception as e:
            print(f"[{datetime.now()}] [SchedulerService] Error en scraping programado: {e}")
    
    def get_cached_data(self):
        """
        Obtiene los datos en caché
        
        Returns:
            dict: Datos en caché
        """
        return self.cached_data
    
    def set_cached_data(self, data):
        """
        Actualiza los datos en caché
        
        Args:
            data (dict): Nuevos datos
        """
        self.cached_data = data
    
    def update_interval(self, interval_minutes):
        """
        Actualiza el intervalo de scraping
        
        Args:
            interval_minutes (int): Nuevo intervalo en minutos
        """
        try:
            if self.is_running:
                # Eliminar tarea existente
                self.scheduler.remove_job('scrape_job')
                
                # Agregar nueva tarea con nuevo intervalo
                self.scheduler.add_job(
                    self.scheduled_scrape,
                    'interval',
                    minutes=interval_minutes,
                    id='scrape_job',
                    name='INEGI Scheduled Scraping'
                )
                
                print(f"[{datetime.now()}] [SchedulerService] Intervalo actualizado a {interval_minutes} minuto(s)")
                return True
            else:
                print(f"[{datetime.now()}] [SchedulerService] Scheduler no está ejecutándose")
                return False
                
        except Exception as e:
            print(f"[{datetime.now()}] [SchedulerService] Error actualizando intervalo: {e}")
            return False
    
    def get_status(self):
        """
        Obtiene el estado del scheduler
        
        Returns:
            dict: Estado del scheduler
        """
        jobs = self.scheduler.get_jobs() if self.is_running else []
        
        return {
            'is_running': self.is_running,
            'jobs_count': len(jobs),
            'has_cached_data': len(self.cached_data) > 0,
            'last_update': self.cached_data.get('timestamp', 'N/A') if self.cached_data else 'N/A'
        }
