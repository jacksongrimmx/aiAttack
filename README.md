# INEGI Web Scraper

Sistema de web scraping para extraer información del sitio oficial del INEGI (Instituto Nacional de Estadística y Geografía de México).

## ⏰ Cron Job Automático

El sistema ejecuta scraping automático **cada 5 minutos** mediante un scheduler integrado.

## 🏗️ Arquitectura de Microservicios

Este proyecto está diseñado con una **arquitectura modular de microservicios**:

### Servicios Principales:
- **ScraperService** - Servicio de web scraping especializado
- **StorageService** - Servicio de persistencia y almacenamiento
- **SchedulerService** - Servicio de tareas programadas (Cron Job cada 5 min)
- **API REST** - Endpoints para interactuar con los servicios

## 📋 Descripción

El sistema extrae automáticamente:
- Título del sitio
- Secciones principales
- Últimas noticias y comunicados
- Indicadores destacados
- Links importantes

## 🚀 Instalación

1. Activa el entorno virtual (si aún no está activado):
```powershell
.\venv\Scripts\Activate.ps1
```

2. Las dependencias ya están instaladas. Si necesitas reinstalarlas:
```powershell
pip install -r requirements.txt
```

## 📦 Estructura del Proyecto

```
aiAttack/
├── app.py                      # Aplicación principal
├── config.py                   # Configuración centralizada
├── scraper.py                  # Scraper legacy (mantener compatibilidad)
├── requirements.txt            # Dependencias
│
├── services/                   # 🔥 Microservicios
│   ├── __init__.py
│   ├── scraper_service.py     # Servicio de web scraping
│   ├── storage_service.py     # Servicio de almacenamiento
│   └── scheduler_service.py   # Servicio de programación
│inmediatamente |
| `/api/data` | GET | Obtener datos en caché |
| `/api/data/json` | GET | Descargar archivo JSON |
| `/api/data/csv` | GET | Descargar archivo CSV |
| `/api/status` | GET | Estado completo del sistema |
| `/api/files` | GET | Listar archivos de datos |
| `/api/schedule` | POST | Configurar intervalo de scraping
│   └── __init__.py
│
├── data/                       # Datos generados
│   ├── inegi_data.json
│   ├── inegi_data.csv
│   └── inegi_latest.json
│
└── tests/
    ├── test_scraper.py
    └── test_microservices.py  # 🔥 Test de microservicios
```

## 🔧 Microservicios

### 1. **ScraperService** (`services/scraper_service.py`)
Servicio especializado en web scraping:
- Conexión HTTP con headers apropiados
- Parsing de HTML con BeautifulSoup
- Extracción de datos estructurados
- Manejo de errores robusto

### 2. **StorageService** (`services/storage_service.py`)
Servicio de persistencia de datos:
- Guardar en formato JSON
- Guardar en formato CSV
- Cargar datos existentes
- Gestión de archivos

### 3. **SchedulerService** (`services/scheduler_service.py`)
Servicio de tareas programadas:
- Scraping automático con intervalo configurable
- Caché de datos en memoria
- Control de jobs (start/stop/update)
- Estado del scheduler

### 4. **API REST** (`api/routes.py`)
Endpoints HTTP para interactuar con los servicios:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información de la API |
| `/api/scrape` | GET | Ejecutar scraping ahora |
| `/api/data` | GET | Obtener datos en caché |
| `/api/data/json` | GET | Descargar archivo JSON |
| `/api/data/csv` | GET | Descargar archivo CSV |
| `/api/status` | GET | Estado del scraper |
| `/api/schedule` | POST | Configurar frecuencia |

## 🎮 Uso
 (Recomendado)

```powershell
python app.py
```

La API iniciará en `http://localhost:5000` con todos los microservicios activos.

### Opción 2: Usar los microservicios directamente

```python
from services import ScraperService, StorageService, SchedulerService
from config import Config

# Inicializar servicios
scraper = ScraperService()
storage = StorageService()
scheduler = SchedulerService(scraper, storage)

# Ejecutar scraping
data = scraper.scrape_homepage()

# Guardar datos
storage.save_json(data)
storage.save_csv(data)

# Iniciar scraping automático
scheduler.start(interval_hours=1)
```

### Opción 3: Ejecutar pruebas

```powershell
# Prueba del scraper legacy
python test_scraper.py

# Prueba de microservicios
python test_microservices.py
```

### Opción 4: Usar la API con curl

```bash
# Obtener información
curl http://localhost:5000/

# Ejecutar scraping
curl http://localhost:5000/api/scrape

# Obtener datos
curl http://localhost:5000/api/data

# Ver estado del sistema
curl http://localhost:5000/api/status

# Configurar intervalo (2 horas)
curl -X POST http://localhost:5000/api/schedule \
  -H "Content-Type: applica para API REST
- **BeautifulSoup4** - Parsing HTML
- **Requests** - Peticiones HTTP
- **APScheduler** - Tareas programadas
- **Flask-CORS** - Cross-Origin Resource Sharing

## 🎯 Ventajas de la Arquitectura de Microservicios

✅ **Separación de responsabilidades** - Cada servicio tiene una función específica  
✅ **Mantenibilidad** - Código organizado y fácil de modificar  
✅ **Testabilidad** - Cada servicio puede probarse independientemente  
✅ **Escalabilidad** - Los servicios pueden crecer o separarse en procesos independientes  
✅ **Reutilización** - Los servicios pueden usarse en otros proyectos  
✅ **Configuración centralizada** - Un solo lugar para toda la configuración
## 📁 Estructura de Datos

El scraper extrae y devuelve:

```json
{
  "timestamp": "2025-12-15T20:12:04.664509",
  "url": "https://www.inegi.org.mx",
  "title": "Instituto Nacional de Estadística y Geografía (INEGI)",
  "status": "success",
  "main_sections": [],
  "latest_news": [],
  "featured_indicators": [],
  "links": []
}
```

## 📂 Archivos Generados

Los datos se guardan en la carpeta `data/`:
- `inegi_data.json` - Datos en formato JSON
- `inegi_data.csv` - Datos en formato CSV
- `inegi_latest.json` - Última ejecución programada

## 🛠️ Tecnologías

- **Python 3.12**
- **Flask** - Framework web
- **BeautifulSoup4** - Parsing HTML
- **Requests** - Peticiones HTTP
- **APScheduler** - Tareas programadas
- **Flask-CORS** - Cross-Origin Resource Sharing

## ⚙️ Configuración

La API está configurada en `config.py`:
- ⏰ **Cron Job automático cada 5 minutos** (configurable)
- Timeout de conexión: **30 segundos**
- Puerto: **5000**
- Host: **0.0.0.0** (accesible desde la red local)

### Cambiar el intervalo del Cron Job:

1. **Editar config.py**:
```python
SCRAPING_INTERVAL_MINUTES = 10  # Cambiar a 10 minutos
```

2. **O usar la API**:
```powershell
# Cambiar a 10 minutos
Invoke-RestMethod -Uri "http://localhost:5000/api/schedule" -Method POST -Body '{"interval_minutes": 10}' -ContentType "application/json"
```

## 📝 Notas

- El scraper respeta el sitio web usando User-Agent apropiado
- Los datos extraídos dependen de la estructura actual del sitio del INEGI
- Si el sitio cambia su estructura, puede ser necesario ajustar los selectores

## 🐛 Solución de Problemas

**Error: ModuleNotFoundError**
```powershell
pip install -r requirements.txt
```

**Error: Connection refused**
- Verifica tu conexión a internet
- El sitio del INEGI puede estar temporalmente no disponible

**La API no responde**
- Verifica que no haya otra aplicación usando el puerto 5000
- Revisa los logs en la terminal

## 📄 Licencia

Proyecto educativo/personal. Respeta los términos de uso del sitio del INEGI.
