"""
Servicio de Almacenamiento - Microservicio para persistencia de datos
"""
import json
import csv
import os
from datetime import datetime
from config import Config


class StorageService:
    """Servicio especializado en almacenamiento y exportación de datos"""
    
    def __init__(self):
        self.data_dir = Config.DATA_DIR
        Config.init_app()  # Asegurar que el directorio existe
    
    def save_json(self, data, filename=None):
        """
        Guarda datos en formato JSON
        
        Args:
            data (dict): Datos a guardar
            filename (str): Nombre del archivo (opcional)
            
        Returns:
            bool: True si se guardó exitosamente
        """
        if filename is None:
            filename = Config.JSON_FILENAME
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"[{datetime.now()}] [StorageService] JSON guardado: {filepath}")
            return True
            
        except Exception as e:
            print(f"[{datetime.now()}] [StorageService] Error guardando JSON: {e}")
            return False
    
    def save_csv(self, data, filename=None):
        """
        Guarda datos en formato CSV
        
        Args:
            data (dict): Datos a guardar
            filename (str): Nombre del archivo (opcional)
            
        Returns:
            bool: True si se guardó exitosamente
        """
        if filename is None:
            filename = Config.CSV_FILENAME
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Información básica
                writer.writerow(['Campo', 'Valor'])
                writer.writerow(['Timestamp', data.get('timestamp', '')])
                writer.writerow(['URL', data.get('url', '')])
                writer.writerow(['Status', data.get('status', '')])
                writer.writerow(['Título', data.get('title', '')])
                
                # Secciones principales
                writer.writerow([])
                writer.writerow(['=== SECCIONES PRINCIPALES ==='])
                writer.writerow(['Nombre', 'URL'])
                for section in data.get('main_sections', []):
                    writer.writerow([section.get('name', ''), section.get('url', '')])
                
                # Noticias
                writer.writerow([])
                writer.writerow(['=== ÚLTIMAS NOTICIAS ==='])
                writer.writerow(['Título', 'URL', 'Fecha'])
                for news in data.get('latest_news', []):
                    writer.writerow([
                        news.get('title', ''), 
                        news.get('url', ''), 
                        news.get('date', '')
                    ])
                
                # Indicadores
                writer.writerow([])
                writer.writerow(['=== INDICADORES DESTACADOS ==='])
                writer.writerow(['Indicador'])
                for indicator in data.get('featured_indicators', []):
                    writer.writerow([indicator])
                
                # Links importantes
                writer.writerow([])
                writer.writerow(['=== LINKS IMPORTANTES ==='])
                writer.writerow(['Texto', 'URL'])
                for link in data.get('important_links', []):
                    writer.writerow([link.get('text', ''), link.get('url', '')])
            
            print(f"[{datetime.now()}] [StorageService] CSV guardado: {filepath}")
            return True
            
        except Exception as e:
            print(f"[{datetime.now()}] [StorageService] Error guardando CSV: {e}")
            return False
    
    def load_json(self, filename=None):
        """
        Carga datos desde archivo JSON
        
        Args:
            filename (str): Nombre del archivo (opcional)
            
        Returns:
            dict: Datos cargados o None si hay error
        """
        if filename is None:
            filename = Config.JSON_FILENAME
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"[{datetime.now()}] [StorageService] JSON cargado: {filepath}")
                return data
            else:
                print(f"[{datetime.now()}] [StorageService] Archivo no encontrado: {filepath}")
                return None
                
        except Exception as e:
            print(f"[{datetime.now()}] [StorageService] Error cargando JSON: {e}")
            return None
    
    def file_exists(self, filename):
        """
        Verifica si un archivo existe
        
        Args:
            filename (str): Nombre del archivo
            
        Returns:
            bool: True si existe
        """
        filepath = os.path.join(self.data_dir, filename)
        return os.path.exists(filepath)
    
    def get_file_path(self, filename):
        """
        Obtiene la ruta completa de un archivo
        
        Args:
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta completa del archivo
        """
        return os.path.join(self.data_dir, filename)
    
    def list_data_files(self):
        """
        Lista todos los archivos en el directorio de datos
        
        Returns:
            list: Lista de nombres de archivos
        """
        try:
            if os.path.exists(self.data_dir):
                return os.listdir(self.data_dir)
            return []
        except Exception as e:
            print(f"[{datetime.now()}] [StorageService] Error listando archivos: {e}")
            return []
