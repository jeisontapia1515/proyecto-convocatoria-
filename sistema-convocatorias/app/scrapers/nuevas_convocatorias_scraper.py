
from typing import List, Dict
from app.scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger('scraping')


class FondoCaldasScraper(BaseScraper):
    """
    Scraper para convocatorias del Fondo Caldas
    """
    
    def __init__(self):
        super().__init__(
            fuente_nombre="Fondo Caldas",
            url="https://www.fondocaldas.com/convocatorias/"
        )
    
    def extract_convocatorias(self) -> List[Dict]:
        """
        Extrae convocatorias del Fondo Caldas
        """
        convocatorias = []
        
        html = self.fetch_page(self.url)
        if not html:
            return convocatorias
            
        soup = self.parse_html(html)
        
        print(soup.prettify())
        
        # TODO: Implementar la lógica de extracción específica para el Fondo Caldas
        
        return convocatorias
