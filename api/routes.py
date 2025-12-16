"""
API Routes - Endpoints de la aplicación
"""
from flask import jsonify, request, send_file
from datetime import datetime
from config import Config


def create_routes(app, scraper_service, storage_service, scheduler_service):
    """
    Crea y registra todas las rutas de la API
    
    Args:
        app: Instancia de Flask
        scraper_service: Servicio de scraping
        storage_service: Servicio de almacenamiento
        scheduler_service: Servicio de programación
    """
    
    @app.route('/')
    def home():
        """Información general de la API"""
        return jsonify({
            'service': 'INEGI Web Scraper API',
            'version': '2.0 - Microservices',
            'description': 'API REST para extraer datos del INEGI mediante web scraping',
            'architecture': 'Microservicios',
            'endpoints': {
                'GET /': 'Información de la API',
                'GET /api/scrape': 'Ejecutar scraping inmediatamente',
                'GET /api/data': 'Obtener datos en caché',
                'GET /api/data/json': 'Descargar archivo JSON',
                'GET /api/data/csv': 'Descargar archivo CSV',
                'GET /api/status': 'Estado del sistema',
                'GET /api/files': 'Listar archivos de datos',
                'POST /api/schedule': 'Configurar intervalo de scraping'
            },
            'services': {
                'scraper': 'Servicio de web scraping',
                'storage': 'Servicio de almacenamiento',
                'scheduler': 'Servicio de tareas programadas'
            }
        }), 200
    
    @app.route('/api/scrape', methods=['GET'])
    def scrape_now():
        """Ejecutar scraping inmediatamente"""
        try:
            print(f"[{datetime.now()}] [API] Scraping manual solicitado")
            
            # Ejecutar scraping
            data = scraper_service.scrape_homepage()
            
            if data.get('status') == 'success':
                # Guardar datos
                storage_service.save_json(data)
                storage_service.save_csv(data)
                
                # Actualizar caché
                scheduler_service.set_cached_data(data)
                
                return jsonify({
                    'status': 'success',
                    'message': 'Scraping completado exitosamente',
                    'data': data
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Error durante el scraping',
                    'data': data
                }), 500
                
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Error interno: {str(e)}'
            }), 500
    
    @app.route('/api/data', methods=['GET'])
    def get_cached_data():
        """Obtener datos en caché"""
        cached_data = scheduler_service.get_cached_data()
        
        if cached_data:
            return jsonify({
                'status': 'success',
                'source': 'cache',
                'data': cached_data
            }), 200
        
        # Intentar cargar desde archivo
        data = storage_service.load_json(Config.LATEST_JSON)
        if data:
            scheduler_service.set_cached_data(data)
            return jsonify({
                'status': 'success',
                'source': 'file',
                'data': data
            }), 200
        
        return jsonify({
            'status': 'error',
            'message': 'No hay datos disponibles. Ejecuta /api/scrape primero'
        }), 404
    
    @app.route('/api/data/json', methods=['GET'])
    def download_json():
        """Descargar archivo JSON"""
        try:
            filepath = storage_service.get_file_path(Config.JSON_FILENAME)
            
            if storage_service.file_exists(Config.JSON_FILENAME):
                return send_file(
                    filepath,
                    mimetype='application/json',
                    as_attachment=True,
                    download_name=f'inegi_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                )
            
            return jsonify({
                'status': 'error',
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @app.route('/api/data/csv', methods=['GET'])
    def download_csv():
        """Descargar archivo CSV"""
        try:
            filepath = storage_service.get_file_path(Config.CSV_FILENAME)
            
            if storage_service.file_exists(Config.CSV_FILENAME):
                return send_file(
                    filepath,
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=f'inegi_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                )
            
            return jsonify({
                'status': 'error',
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @app.route('/api/status', methods=['GET'])
    def get_status():
        """Estado del sistema"""
        scheduler_status = scheduler_service.get_status()
        files = storage_service.list_data_files()
        
        return jsonify({
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'scheduler': scheduler_status,
            'storage': {
                'json_exists': storage_service.file_exists(Config.JSON_FILENAME),
                'csv_exists': storage_service.file_exists(Config.CSV_FILENAME),
                'latest_exists': storage_service.file_exists(Config.LATEST_JSON),
                'total_files': len(files),
                'files': files
            },
            'config': {
                'scraping_interval_minutes': Config.SCRAPING_INTERVAL_MINUTES,
                'inegi_url': Config.INEGI_BASE_URL,
                'data_directory': Config.DATA_DIR
            }
        }), 200
    
    @app.route('/api/files', methods=['GET'])
    def list_files():
        """Listar todos los archivos de datos"""
        files = storage_service.list_data_files()
        
        return jsonify({
            'status': 'success',
            'count': len(files),
            'files': files,
            'data_directory': Config.DATA_DIR
        }), 200
    
    @app.route('/api/schedule', methods=['POST'])
    def configure_schedule():
        """Configurar intervalo de scraping"""
        try:
            data = request.get_json()
            
            if not data or 'interval_minutes' not in data:
                return jsonify({
                    'status': 'error',
                    'message': 'Se requiere el parámetro interval_minutes'
                }), 400
            
            interval_minutes = data['interval_minutes']
            
            if not isinstance(interval_minutes, (int, float)) or interval_minutes <= 0:
                return jsonify({
                    'status': 'error',
                    'message': 'interval_minutes debe ser un número positivo'
                }), 400
            
            success = scheduler_service.update_interval(interval_minutes)
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': f'Intervalo actualizado correctamente',
                    'interval_minutes': interval_minutes
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'No se pudo actualizar el intervalo'
                }), 500
                
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Manejo de errores 404"""
        return jsonify({
            'status': 'error',
            'message': 'Endpoint no encontrado',
            'code': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Manejo de errores 500"""
        return jsonify({
            'status': 'error',
            'message': 'Error interno del servidor',
            'code': 500
        }), 500
