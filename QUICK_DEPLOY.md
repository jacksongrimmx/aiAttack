# 🚀 Despliegue Rápido en Heroku

## Comandos para desplegar:

```powershell
# 1. Login en Heroku
heroku login

# 2. Crear app
heroku create inegi-scraper-tu-nombre

# 3. Hacer commit de cambios
git add .
git commit -m "Configuración para Heroku"

# 4. Desplegar
git push heroku main

# 5. Ver logs
heroku logs --tail

# 6. Abrir la app
heroku open
```

## Verificar que funciona:

```powershell
# Reemplaza 'tu-app-name' con el nombre de tu app
curl https://tu-app-name.herokuapp.com/api/status
```

## ✅ Archivos creados para Heroku:
- ✅ `Procfile` - Configuración de proceso
- ✅ `runtime.txt` - Versión de Python
- ✅ `.slugignore` - Archivos a ignorar
- ✅ `requirements.txt` - Dependencias (con gunicorn)
- ✅ `config.py` - Actualizado para usar PORT de Heroku
- ✅ `app.py` - Scheduler se inicia automáticamente

## 📖 Documentación completa:
Ver `DEPLOY_HEROKU.md` para instrucciones detalladas.
