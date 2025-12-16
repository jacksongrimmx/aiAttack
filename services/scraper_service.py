"""
Servicio de Web Scraping - Microservicio para extraer datos del INEGI
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from config import Config


class ScraperService:
    """Servicio especializado en scraping del sitio INEGI"""
    
    def __init__(self):
        self.base_url = Config.INEGI_BASE_URL
        self.headers = {'User-Agent': Config.USER_AGENT}
        self.timeout = Config.REQUEST_TIMEOUT
        
    def scrape_homepage(self):
        """
        Extrae información de la página principal del INEGI
        
        Returns:
            dict: Datos extraídos del sitio
        """
        try:
            print(f"[{datetime.now()}] [ScraperService] Iniciando scraping de {self.base_url}...")
            
            # Realizar petición HTTP
            response = self._make_request()
            if not response:
                return self._error_response('Error al conectar con el sitio')
            
            # Parsear HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer datos
            data = {
                'timestamp': datetime.now().isoformat(),
                'url': self.base_url,
                'title': self._extract_title(soup),
                'main_sections': self._extract_sections(soup),
                'latest_news': self._extract_news(soup),
                'featured_indicators': self._extract_indicators(soup),
                'important_links': self._extract_links(soup),
                'status': 'success'
            }
            
            print(f"[{datetime.now()}] [ScraperService] Scraping completado exitosamente")
            print(f"  - Secciones: {len(data['main_sections'])}")
            print(f"  - Noticias: {len(data['latest_news'])}")
            print(f"  - Indicadores: {len(data['featured_indicators'])}")
            print(f"  - Links: {len(data['important_links'])}")
            
            return data
            
        except Exception as e:
            print(f"[{datetime.now()}] [ScraperService] Error: {e}")
            return self._error_response(str(e))
    
    def _make_request(self):
        """Realizar petición HTTP al sitio"""
        try:
            response = requests.get(
                self.base_url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response
        except requests.RequestException as e:
            print(f"[{datetime.now()}] [ScraperService] Error de conexión: {e}")
            return None
    
    def _extract_title(self, soup):
        """Extrae el título de la página"""
        try:
            title = soup.find('title')
            return title.text.strip() if title else "Sin título"
        except Exception as e:
            print(f"[ScraperService] Error extrayendo título: {e}")
            return "Error al extraer título"
    
    def _extract_sections(self, soup):
        """Extrae las secciones principales del sitio"""
        sections = []
        try:
            nav_items = soup.find_all(
                ['nav', 'ul', 'div'], 
                class_=lambda x: x and ('menu' in x.lower() or 'nav' in x.lower())
            )
            
            for nav in nav_items[:3]:
                links = nav.find_all('a', href=True)
                for link in links[:10]:
                    text = link.get_text(strip=True)
                    if text and len(text) > 3:
                        sections.append({
                            'name': text,
                            'url': self._normalize_url(link['href'])
                        })
            
            # Eliminar duplicados
            sections = list({s['name']: s for s in sections}.values())
            
        except Exception as e:
            print(f"[ScraperService] Error extrayendo secciones: {e}")
        
        return sections[:Config.MAX_SECTIONS]
    
    def _extract_news(self, soup):
        """Extrae las últimas noticias o comunicados"""
        news = []
        try:
            news_sections = soup.find_all(
                ['article', 'div', 'section'], 
                class_=lambda x: x and ('noticia' in x.lower() or 'comunicado' in x.lower() or 'news' in x.lower())
            )
            
            for item in news_sections[:10]:
                title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = item.find('a', href=True)
                    
                    news.append({
                        'title': title,
                        'url': self._normalize_url(link['href'] if link else ''),
                        'date': self._extract_date(item)
                    })
            
        except Exception as e:
            print(f"[ScraperService] Error extrayendo noticias: {e}")
        
        return news[:Config.MAX_NEWS]
    
    def _extract_indicators(self, soup):
        """Extrae indicadores destacados"""
        indicators = []
        try:
            indicator_sections = soup.find_all(
                ['div', 'section'], 
                class_=lambda x: x and ('indicador' in x.lower() or 'indicator' in x.lower() or 'estadistica' in x.lower())
            )
            
            for item in indicator_sections[:10]:
                text = item.get_text(strip=True)
                if text and len(text) < 500:
                    indicators.append(text)
            
        except Exception as e:
            print(f"[ScraperService] Error extrayendo indicadores: {e}")
        
        return indicators[:Config.MAX_INDICATORS]
    
    def _extract_links(self, soup):
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
                        'url': self._normalize_url(href)
                    })
            
            # Eliminar duplicados
            links = list({l['text']: l for l in links}.values())
            
        except Exception as e:
            print(f"[ScraperService] Error extrayendo links: {e}")
        
        return links[:Config.MAX_LINKS]
    
    def _extract_date(self, element):
        """Intenta extraer una fecha del elemento"""
        try:
            date_elem = element.find(
                ['time', 'span'], 
                class_=lambda x: x and 'fecha' in x.lower() if x else False
            )
            if date_elem:
                return date_elem.get_text(strip=True)
        except:
            pass
        return "N/A"
    
    def _normalize_url(self, url):
        """Normaliza URLs relativas a absolutas"""
        if not url:
            return 'N/A'
        return url if url.startswith('http') else f"{self.base_url}{url}"
    
    def _error_response(self, error_message):
        """Genera respuesta de error estandarizada"""
        return {
            'timestamp': datetime.now().isoformat(),
            'url': self.base_url,
            'status': 'error',
            'error': error_message,
            'main_sections': [],
            'latest_news': [],
            'featured_indicators': [],
            'important_links': []
        }
