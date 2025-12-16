# Configuración de Cron Job - Scraping cada 5 minutos

## ✅ Cambios Realizados

### 1. Archivo de Configuración (`config.py`)
```python
# Antes:
SCRAPING_INTERVAL_HOURS = 1  # Cada hora

# Ahora:
SCRAPING_INTERVAL_MINUTES = 5  # Cada 5 minutos
```

### 2. Servicio de Programación (`services/scheduler_service.py`)
- ✓ Método `start()` actualizado para usar minutos
- ✓ Método `update_interval()` actualizado para usar minutos
- ✓ Mensajes de log actualizados

### 3. API REST (`api/routes.py`)
- ✓ Endpoint `/api/status` muestra intervalo en minutos
- ✓ Endpoint `/api/schedule` acepta `interval_minutes` en lugar de `interval_hours`

### 4. Aplicación Principal (`app.py`)
- ✓ Completamente reescrita sin código duplicado
- ✓ Usa `SCRAPING_INTERVAL_MINUTES` de la configuración
- ✓ Muestra mensaje claro sobre el intervalo de 5 minutos

## 🎯 Cómo Usar

### Iniciar con Cron Job automático:
```powershell
python app.py
```

El sistema ejecutará automáticamente el scraping cada 5 minutos.

### Probar el Cron Job:
```powershell
python test_cron_job.py
```

Este script te mostrará en tiempo real cada ejecución automática.

### Cambiar el intervalo dinámicamente:

#### Opción 1: Usando curl/PowerShell
```powershell
# Cambiar a 10 minutos
curl -X POST http://localhost:5000/api/schedule -H "Content-Type: application/json" -d '{"interval_minutes": 10}'
```

#### Opción 2: Usando Invoke-RestMethod
```powershell
$body = @{ interval_minutes = 10 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api/schedule" -Method POST -Body $body -ContentType "application/json"
```

## 📊 Verificar Estado

### Ver estado del sistema:
```powershell
curl http://localhost:5000/api/status
```

Respuesta:
```json
{
  "status": "running",
  "scheduler": {
    "is_running": true,
    "jobs_count": 1,
    "has_cached_data": true,
    "last_update": "2025-12-15T20:35:06.664509"
  },
  "storage": {
    "json_exists": true,
    "csv_exists": true,
    "latest_exists": true,
    "total_files": 3
  },
  "config": {
    "scraping_interval_minutes": 5,
    "inegi_url": "https://www.inegi.org.mx"
  }
}
```

## 🔍 Logs en Consola

Al iniciar la aplicación verás:
```
============================================================
🚀 API REST DISPONIBLE - Cron Job cada 5 minutos
============================================================
⏰ Scraping automático cada 5 minutos
============================================================
```

Cada 5 minutos verás en los logs:
```
[2025-12-15 20:40:05.826485] [SchedulerService] Ejecutando scraping programado...
[2025-12-15 20:40:06.200486] [ScraperService] Scraping completado exitosamente
```

## 📝 Notas Importantes

- El cron job es **persistente**: Mientras la aplicación esté corriendo, el scraping se ejecutará automáticamente
- **Primera ejecución**: Ocurre inmediatamente al iniciar la aplicación
- **Siguientes ejecuciones**: Cada 5 minutos desde la primera ejecución
- Los datos se guardan automáticamente en `data/` en cada ejecución
