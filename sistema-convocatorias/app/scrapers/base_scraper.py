"""
Clase base para todos los scrapers
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import logging
import hashlib
from datetime import datetime
from app.utils.config import settings

logger = logging.getLogger('scraping')


class BaseScraper(ABC):
    """
    Clase base para implementar scrapers de diferentes fuentes
    """
    
    def __init__(self, fuente_nombre: str, url: str):
        self.fuente_nombre = fuente_nombre
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.USER_AGENT
        })
        if settings.proxies:
            self.session.proxies.update(settings.proxies)
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Obtiene el contenido HTML de una página
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(
                url,
                timeout=settings.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parsea HTML con BeautifulSoup
        """
        return BeautifulSoup(html, 'html.parser')
    
    @abstractmethod
    def extract_convocatorias(self) -> List[Dict]:
        """
        Método abstracto que cada scraper debe implementar
        Retorna lista de diccionarios con datos de convocatorias
        """
        pass
    
    def create_hash(self, texto: str) -> str:
        """
        Crea hash MD5 de un texto para detectar duplicados
        """
        return hashlib.md5(texto.encode('utf-8')).hexdigest()
    
    def clean_text(self, text: str) -> str:
        """
        Limpia texto eliminando espacios extras y caracteres especiales
        """
        if not text:
            return ""
        # Eliminar espacios múltiples
        text = ' '.join(text.split())
        return text.strip()
    
    def extract_date(self, date_text: str) -> Optional[datetime]:
        """
        Intenta extraer fecha de texto en varios formatos
        """
        if not date_text:
            return None
        
        date_formats = [
            "%d/%m/%Y",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d de %B de %Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
        ]
        
        # Reemplazar nombres de meses en español
        meses = {
            'enero': 'january', 'febrero': 'february', 'marzo': 'march',
            'abril': 'april', 'mayo': 'may', 'junio': 'june',
            'julio': 'july', 'agosto': 'august', 'septiembre': 'september',
            'octubre': 'october', 'noviembre': 'november', 'diciembre': 'december'
        }
        
        # Días de la semana para eliminar
        dias = ['lunes', 'martes', 'miércoles', 'miercoles', 'jueves', 'viernes', 'sábado', 'sabado', 'domingo']
        
        date_text_lower = date_text.lower()
        
        # Eliminar días de la semana y comas asociadas
        for dia in dias:
            date_text_lower = date_text_lower.replace(dia + ',', '').replace(dia, '').strip()
            
        for esp, eng in meses.items():
            date_text_lower = date_text_lower.replace(esp, eng)
        
        # Limpiar espacios múltiples de nuevo
        date_text_lower = ' '.join(date_text_lower.split())

        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_text_lower, fmt)
            except:
                continue
        
        logger.warning(f"No se pudo parsear fecha: {date_text}")
        return None
    
    def run(self) -> List[Dict]:
        """
        Ejecuta el scraper y retorna resultados
        """
        logger.info(f"Iniciando scraping de {self.fuente_nombre}")
        try:
            convocatorias = self.extract_convocatorias()
            logger.info(f"✅ {len(convocatorias)} convocatorias extraídas de {self.fuente_nombre}")
            return convocatorias
        except Exception as e:
            logger.error(f"❌ Error en scraping de {self.fuente_nombre}: {e}", exc_info=True)
            return []
