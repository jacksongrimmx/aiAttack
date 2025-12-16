"""Script de prueba para el scraper del INEGI"""
from scraper import INEGIScraper
import json

if __name__ == '__main__':
    print("="*60)
    print("PRUEBA DEL SCRAPER DEL INEGI")
    print("="*60)
    
    # Crear instancia del scraper
    scraper = INEGIScraper()
    print(f"✓ Scraper creado")
    print(f"✓ URL objetivo: {scraper.base_url}")
    print()
    
    # Ejecutar scraping
    print("Iniciando scraping del sitio del INEGI...")
    print("-"*60)
    data = scraper.scrape_homepage()
    
    # Mostrar resultados
    print()
    print("RESULTADOS:")
    print("-"*60)
    print(f"Estado: {data.get('status')}")
    print(f"Timestamp: {data.get('timestamp')}")
    print(f"Título: {data.get('title', 'N/A')}")
    print(f"\nSecciones encontradas: {len(data.get('main_sections', []))}")
    print(f"Noticias encontradas: {len(data.get('latest_news', []))}")
    print(f"Indicadores encontrados: {len(data.get('featured_indicators', []))}")
    print(f"Links importantes: {len(data.get('links', []))}")
    
    # Mostrar algunas secciones
    if data.get('main_sections'):
        print("\nPrimeras 5 secciones:")
        for i, section in enumerate(data['main_sections'][:5], 1):
            print(f"  {i}. {section['name']}")
    
    # Guardar datos
    print("\n" + "-"*60)
    print("Guardando datos...")
    scraper.save_to_json(data)
    scraper.save_to_csv(data)
    
    print("\n" + "="*60)
    print("PRUEBA COMPLETADA EXITOSAMENTE")
    print("="*60)
