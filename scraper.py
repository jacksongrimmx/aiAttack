import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
import os


class INEGIScraper:
    """Web scraper para extraer información del sitio del INEGI"""
    
    def __init__(self):
        self.base_url = "https://www.inegi.org.mx"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def scrape_homepage(self):
        """
        Extrae información de la página principal del INEGI
        """
        try:
            print(f"[{datetime.now()}] Iniciando scraping de INEGI...")
            
            # Realizar petición HTTP
            response = requests.get(self.base_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            # Parsear HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer datos
            data = {
                'timestamp': datetime.now().isoformat(),
                'url': self.base_url,
                'title': self._get_title(soup),
                'main_sections': self._get_main_sections(soup),
                'latest_news': self._get_latest_news(soup),
                'featured_indicators': self._get_featured_indicators(soup),
                'links': self._get_important_links(soup),
                'status': 'success'
            }
            
            print(f"[{datetime.now()}] Scraping completado exitosamente")
            return data
            
        except requests.RequestException as e:
            print(f"[{datetime.now()}] Error de conexión: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'url': self.base_url,
                'status': 'error',
                'error': f'Error de conexión: {str(e)}'
            }
        except Exception as e:
            print(f"[{datetime.now()}] Error general: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'url': self.base_url,
                'status': 'error',
                'error': f'Error general: {str(e)}'
            }
    
    def _get_title(self, soup):
        """Extrae el título de la página"""
        try:
            title = soup.find('title')
            return title.text.strip() if title else "No title found"
        except:
            return "Error extracting title"
    
    def _get_main_sections(self, soup):
        """Extrae las secciones principales del sitio"""
        sections = []
        try:
            # Buscar menú principal o secciones destacadas
            nav_items = soup.find_all(['nav', 'ul', 'div'], class_=lambda x: x and ('menu' in x.lower() or 'nav' in x.lower()))
            
            for nav in nav_items[:3]:  # Limitar a las primeras 3 estructuras
                links = nav.find_all('a', href=True)
                for link in links[:10]:  # Limitar a 10 links por estructura
                    text = link.get_text(strip=True)
                    if text and len(text) > 3:  # Filtrar textos muy cortos
                        sections.append({
                            'name': text,
                            'url': link['href'] if link['href'].startswith('http') else self.base_url + link['href']
                        })
            
            # Eliminar duplicados
            sections = list({s['name']: s for s in sections}.values())
            
        except Exception as e:
            print(f"Error extrayendo secciones: {e}")
        
        return sections[:15]  # Retornar máximo 15 secciones
    
    def _get_latest_news(self, soup):
        """Extrae las últimas noticias o comunicados"""
        news = []
        try:
            # Buscar secciones de noticias/comunicados
            news_sections = soup.find_all(['article', 'div', 'section'], 
                                         class_=lambda x: x and ('noticia' in x.lower() or 'comunicado' in x.lower() or 'news' in x.lower()))
            
            for item in news_sections[:10]:
                title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = item.find('a', href=True)
                    
                    news.append({
                        'title': title,
                        'url': link['href'] if link and link['href'].startswith('http') else (self.base_url + link['href'] if link else 'N/A'),
                        'date': self._extract_date(item)
                    })
            
        except Exception as e:
            print(f"Error extrayendo noticias: {e}")
        
        return news[:10]
    
    def _get_featured_indicators(self, soup):
        """Extrae indicadores destacados"""
        indicators = []
        try:
            # Buscar elementos que contengan indicadores o estadísticas
            indicator_sections = soup.find_all(['div', 'section'], 
                                              class_=lambda x: x and ('indicador' in x.lower() or 'indicator' in x.lower() or 'estadistica' in x.lower()))
            
            for item in indicator_sections[:10]:
                text = item.get_text(strip=True)
                if text and len(text) < 500:  # Evitar textos muy largos
                    indicators.append(text)
            
        except Exception as e:
            print(f"Error extrayendo indicadores: {e}")
        
        return indicators[:10]
    
    def _get_important_links(self, soup):
        """Extrae links importantes del sitio"""
        links = []
        try:
            all_links = soup.find_all('a', href=True)
            
            important_keywords = ['banco', 'datos', 'estadistica', 'censo', 'informacion', 'consulta']
            
            for link in all_links:
                text = link.get_text(strip=True)
                href = link['href']
                
                if text and any(keyword in text.lower() for keyword in important_keywords):
                    links.append({
                        'text': text,
                        'url': href if href.startswith('http') else self.base_url + href
                    })
            
            # Eliminar duplicados
            links = list({l['text']: l for l in links}.values())
            
        except Exception as e:
            print(f"Error extrayendo links: {e}")
        
        return links[:20]
    
    def _extract_date(self, element):
        """Intenta extraer una fecha del elemento"""
        try:
            date_elem = element.find(['time', 'span'], class_=lambda x: x and 'fecha' in x.lower() if x else False)
            if date_elem:
                return date_elem.get_text(strip=True)
        except:
            pass
        return "N/A"
    
    def save_to_json(self, data, filename='data/inegi_data.json'):
        """Guarda los datos en formato JSON"""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[{datetime.now()}] Datos guardados en {filename}")
            return True
        except Exception as e:
            print(f"[{datetime.now()}] Error guardando JSON: {e}")
            return False
    
    def save_to_csv(self, data, filename='data/inegi_data.csv'):
        """Guarda los datos en formato CSV"""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Headers
                writer.writerow(['Timestamp', 'URL', 'Status', 'Title'])
                
                # Datos básicos
                writer.writerow([
                    data.get('timestamp', ''),
                    data.get('url', ''),
                    data.get('status', ''),
                    data.get('title', '')
                ])
                
                # Secciones
                writer.writerow([])
                writer.writerow(['Secciones Principales'])
                writer.writerow(['Nombre', 'URL'])
                for section in data.get('main_sections', []):
                    writer.writerow([section.get('name', ''), section.get('url', '')])
                
                # Noticias
                writer.writerow([])
                writer.writerow(['Últimas Noticias'])
                writer.writerow(['Título', 'URL', 'Fecha'])
                for news in data.get('latest_news', []):
                    writer.writerow([news.get('title', ''), news.get('url', ''), news.get('date', '')])
            
            print(f"[{datetime.now()}] Datos guardados en {filename}")
            return True
            
        except Exception as e:
            print(f"[{datetime.now()}] Error guardando CSV: {e}")
            return False
