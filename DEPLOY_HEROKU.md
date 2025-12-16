# Despliegue en Heroku

Guía completa para desplegar el INEGI Web Scraper en Heroku.

## 📋 Requisitos Previos

1. **Cuenta de Heroku**
   - Crear cuenta gratuita en [heroku.com](https://heroku.com)

2. **Heroku CLI instalado**
   ```powershell
   # Descargar e instalar desde: https://devcenter.heroku.com/articles/heroku-cli
   
   # Verificar instalación
   heroku --version
   ```

3. **Git configurado**
   ```powershell
   git --version
   ```

## 🚀 Pasos para Desplegar

### 1. Login en Heroku
```powershell
heroku login
```
Esto abrirá tu navegador para autenticarte.

### 2. Crear aplicación en Heroku
```powershell
# Crear app con nombre único (o deja que Heroku genere uno)
heroku create inegi-scraper-app

# O sin nombre específico:
heroku create
```

### 3. Verificar archivos necesarios
Los siguientes archivos ya están creados:
- ✅ `Procfile` - Define cómo ejecutar la app
- ✅ `requirements.txt` - Dependencias Python
- ✅ `runtime.txt` - Versión de Python
- ✅ `.slugignore` - Archivos a ignorar en Heroku

### 4. Commit de cambios (si hay modificaciones)
```powershell
git add .
git commit -m "Configuración para despliegue en Heroku"
```

### 5. Desplegar a Heroku
```powershell
# Empujar código a Heroku
git push heroku main

# Si tu rama principal es 'master':
git push heroku master
```

### 6. Verificar el despliegue
```powershell
# Ver logs
heroku logs --tail

# Abrir la app en el navegador
heroku open

# Ver estado
heroku ps
```

## 🔧 Configuración Adicional

### Variables de Entorno (opcional)
```powershell
# Configurar variables de entorno si necesitas
heroku config:set SCRAPING_INTERVAL=5
heroku config:set DEBUG=False

# Ver todas las variables
heroku config
```

### Escalar dynos
```powershell
# Asegurar que tienes al menos 1 dyno web ejecutándose
heroku ps:scale web=1

# Ver estado
heroku ps
```

## 📊 Endpoints de la API desplegada

Una vez desplegado, tu API estará disponible en:
```
https://tu-app-name.herokuapp.com/
```

### Probar endpoints:
```powershell
# Información de la API
curl https://tu-app-name.herokuapp.com/

# Estado del sistema
curl https://tu-app-name.herokuapp.com/api/status

# Ejecutar scraping
curl https://tu-app-name.herokuapp.com/api/scrape

# Obtener datos
curl https://tu-app-name.herokuapp.com/api/data
```

## ⏰ Cron Job en Heroku

El cron job (cada 5 minutos) funcionará automáticamente porque usamos **APScheduler** que está integrado en la aplicación.

**Importante**: 
- En el plan gratuito de Heroku, los dynos se duermen después de 30 minutos de inactividad
- Para mantener la app activa 24/7, necesitarás un plan de pago (~$7/mes)
- Alternativamente, puedes usar un servicio como [UptimeRobot](https://uptimerobot.com/) para hacer ping cada 5 minutos y mantenerla activa

### Mantener la app activa (Free tier)
Usar un servicio externo que haga ping:
```
https://tu-app-name.herokuapp.com/api/status
```

## 🐛 Solución de Problemas

### Ver logs en tiempo real
```powershell
heroku logs --tail
```

### Error de despliegue
```powershell
# Ver información de la última compilación
heroku builds

# Ver logs de compilación
heroku builds:output
```

### Reiniciar la aplicación
```powershell
heroku restart
```

### Ejecutar comandos en Heroku
```powershell
# Abrir bash en Heroku
heroku run bash

# Ver archivos
heroku run ls -la

# Verificar Python
heroku run python --version
```

## 📈 Monitoreo

### Ver métricas
```powershell
heroku metrics
```

### Ver estado de dynos
```powershell
heroku ps
```

## 💰 Costos

- **Free Tier**: 
  - 550 horas/mes gratis
  - Dyno se duerme después de 30 min de inactividad
  - Perfecto para pruebas

- **Hobby ($7/mes)**:
  - Dyno siempre activo
  - Ideal para producción

- **Professional ($25/mes)**:
  - Métricas avanzadas
  - Múltiples dynos

## 🔄 Actualizar la Aplicación

Cada vez que hagas cambios:
```powershell
git add .
git commit -m "Descripción de cambios"
git push heroku main
```

Heroku automáticamente re-desplegará la aplicación.

## 📝 Notas Importantes

1. **Puerto**: La app usa automáticamente el puerto que Heroku asigna
2. **Datos**: Los archivos guardados en `data/` se perderán al reiniciar (usar base de datos para persistencia)
3. **Timezone**: Heroku usa UTC por defecto
4. **Límites**: El plan gratuito tiene límites de memoria (512MB)

## 🔗 Recursos Útiles

- [Documentación Heroku Python](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Heroku CLI Reference](https://devcenter.heroku.com/articles/heroku-cli)
- [Heroku Scheduler Add-on](https://elements.heroku.com/addons/scheduler) (alternativa a APScheduler)
