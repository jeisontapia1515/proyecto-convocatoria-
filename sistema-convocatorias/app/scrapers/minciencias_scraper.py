"""
Scraper para Minciencias
"""

from typing import List, Dict
from app.scrapers.base_scraper import BaseScraper
import logging
import re

logger = logging.getLogger('scraping')


class MincienciasScraper(BaseScraper):
    """
    Scraper para convocatorias de Minciencias
    URL: https://minciencias.gov.co/convocatorias
    """
    
    def __init__(self):
        super().__init__(
            fuente_nombre="Minciencias",
            url="https://minciencias.gov.co/convocatorias/todas"
        )
    
    def extract_convocatorias(self) -> List[Dict]:
        """
        Extrae convocatorias de Minciencias
        """
        convocatorias = []
        
        # Obtener página principal
        html = self.fetch_page(self.url)
        if not html:
            return convocatorias
        
        soup = self.parse_html(html)
        
        # Buscar contenedores de convocatorias
        # Preferir estructura de tabla si existe
        convocatoria_items = soup.select('table.views-table tbody tr')
        
        if not convocatoria_items:
            # Fallback a estructura de lista (antigua o móvil)
            convocatoria_items = soup.select('.view-content .views-row')
            
        if not convocatoria_items:
            logger.warning("No se encontraron convocatorias con el selector actual")
            # Intentar selector alternativo
            convocatoria_items = soup.select('article.node')
        
        for item in convocatoria_items:
            try:
                # Extraer título (soporte para tabla y lista)
                titulo_elem = item.select_one('h2 a, h3 a, .title a, .views-field-title a')
                if not titulo_elem:
                    continue
                
                titulo = self.clean_text(titulo_elem.get_text())
                url_convocatoria = titulo_elem.get('href', '')
                
                # Hacer URL absoluta
                if url_convocatoria and not url_convocatoria.startswith('http'):
                    url_convocatoria = f"https://minciencias.gov.co{url_convocatoria}"
                
                # Extraer descripción (puede no estar en la tabla)
                descripcion_elem = item.select_one('.field-name-body, .description, p')
                descripcion = self.clean_text(descripcion_elem.get_text()) if descripcion_elem else ""
                
                # Extraer fechas iniciales (de la lista/tabla)
                fecha_apertura = None
                fecha_cierre = None
                
                apertura_elem = item.select_one('.field-name-field-fecha-de-apertura, .fecha-apertura, .views-field-field-fecha-de-apertura')
                if apertura_elem:
                    apertura_text = self.clean_text(apertura_elem.get_text())
                    fecha_apertura = self.extract_date(apertura_text)
                
                # Intentar obtener fecha de cierre de la lista (si existe)
                cierre_elem = item.select_one('.field-name-field-fecha-de-cierre, .fecha-cierre, .views-field-field-fecha-de-cierre')
                if cierre_elem:
                    cierre_text = self.clean_text(cierre_elem.get_text())
                    fecha_cierre = self.extract_date(cierre_text)
                
                # Si no hay fecha de cierre, visitar detalle
                if not fecha_cierre and url_convocatoria:
                    try:
                        logger.info(f"Visitando detalle para {titulo}...")
                        detail_html = self.fetch_page(url_convocatoria)
                        if detail_html:
                            detail_soup = self.parse_html(detail_html)
                            
                            # Buscar fecha cierre en detalle
                            detail_cierre = detail_soup.select_one('.field-name-field-fecha-de-cierre .field-item, .fecha-cierre')
                            if detail_cierre:
                                detail_cierre_text = self.clean_text(detail_cierre.get_text())
                                fecha_cierre = self.extract_date(detail_cierre_text)
                                logger.info(f"Fecha cierre encontrada en detalle: {fecha_cierre}")
                            else:
                                # Buscar en tablas (Cronograma)
                                tables = detail_soup.select('table')
                                for table in tables:
                                    rows = table.select('tr')
                                    for row in rows:
                                        cols = row.select('td, th')
                                        if len(cols) >= 2:
                                            header = self.clean_text(cols[0].get_text()).lower()
                                            value = self.clean_text(cols[1].get_text())
                                            
                                            # Buscar fecha
                                            match = re.search(r'(\d{1,2})\s+(?:de\s+)?([a-zA-Z]+)\s+(?:de\s+)?(\d{4})', value)
                                            if match:
                                                clean_date = f"{match.group(1)} {match.group(2)} {match.group(3)}"
                                                date_obj = self.extract_date(clean_date)
                                                
                                                if date_obj:
                                                    if 'cierre' in header:
                                                        fecha_cierre = date_obj
                                                        logger.info(f"Fecha cierre encontrada en tabla: {fecha_cierre}")
                                                    elif 'apertura' in header and not fecha_apertura:
                                                        fecha_apertura = date_obj
                                                        logger.info(f"Fecha apertura encontrada en tabla: {fecha_apertura}")
                            
                            # Si no teníamos descripción, intentar sacarla del detalle
                            if not descripcion:
                                detail_desc = detail_soup.select_one('.field-name-body .field-item')
                                if detail_desc:
                                    descripcion = self.clean_text(detail_desc.get_text())
                    except Exception as e:
                        logger.error(f"Error visitando detalle de {titulo}: {e}")

                # Determinar estado
                estado = 'abierta'
                # ... (resto del código igual)

                
                # Determinar estado
                estado = 'abierta'
                estado_elem = item.select_one('.estado, .field-name-field-estado')
                if estado_elem:
                    estado_text = self.clean_text(estado_elem.get_text()).lower()
                    if 'cerrada' in estado_text:
                        estado = 'cerrada'
                    elif 'próximamente' in estado_text or 'proximamente' in estado_text:
                        estado = 'proximamente'
                
                # Crear hash para detectar duplicados
                hash_content = self.create_hash(f"{titulo}{url_convocatoria}")
                
                convocatoria = {
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'url': url_convocatoria,
                    'fecha_apertura': fecha_apertura,
                    'fecha_cierre': fecha_cierre,
                    'estado': estado,
                    'hash_contenido': hash_content,
                    'fuente': 'Minciencias'
                }
                
                convocatorias.append(convocatoria)
                logger.debug(f"Extraída: {titulo}")
                
            except Exception as e:
                logger.error(f"Error extrayendo convocatoria: {e}")
                continue
        
        return convocatorias


class SENAScraper(BaseScraper):
    """
    Scraper para convocatorias del SENA
    """
    
    def __init__(self):
        super().__init__(
            fuente_nombre="SENA",
            url="https://www.sena.edu.co/es-co/sennova/Paginas/convocatorias.aspx"
        )
    
    def extract_convocatorias(self) -> List[Dict]:
        """
        Extrae convocatorias del SENA
        """
        convocatorias = []
        
        html = self.fetch_page(self.url)
        if not html:
            return convocatorias
        
        soup = self.parse_html(html)
        
        # Ajustar selectores según estructura real de la página
        items = soup.select('.ms-rtestate-field p, .documento-descargable')
        
        for item in items:
            try:
                # Buscar enlaces en el item
                link = item.find('a')
                if not link:
                    continue
                
                titulo = self.clean_text(link.get_text())
                if not titulo or len(titulo) < 10:
                    continue
                
                url_convocatoria = link.get('href', '')
                if url_convocatoria and not url_convocatoria.startswith('http'):
                    url_convocatoria = f"https://www.sena.edu.co{url_convocatoria}"
                
                # El SENA típicamente publica convocatorias como documentos
                # La descripción puede estar en el texto circundante
                descripcion = self.clean_text(item.get_text())
                
                hash_content = self.create_hash(f"{titulo}{url_convocatoria}")
                
                convocatoria = {
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'url': url_convocatoria,
                    'estado': 'abierta',
                    'hash_contenido': hash_content,
                    'fuente': 'SENA'
                }
                
                convocatorias.append(convocatoria)
                
            except Exception as e:
                logger.error(f"Error extrayendo convocatoria SENA: {e}")
                continue
        
        return convocatorias


class ICETEXScraper(BaseScraper):
    """
    Scraper para convocatorias del ICETEX
    """
    
    def __init__(self):
        super().__init__(
            fuente_nombre="ICETEX",
            url="https://portal.icetex.gov.co/Portal/home/convocatorias"
        )
    
    def extract_convocatorias(self) -> List[Dict]:
        """
        Extrae convocatorias del ICETEX
        """
        convocatorias = []
        
        html = self.fetch_page(self.url)
        if not html:
            return convocatorias
        
        soup = self.parse_html(html)
        
        # Ajustar selectores según la estructura real
        items = soup.select('.convocatoria-item, .card, article')
        
        for item in items:
            try:
                titulo_elem = item.select_one('h2, h3, .titulo, .card-title')
                if not titulo_elem:
                    continue
                
                titulo = self.clean_text(titulo_elem.get_text())
                
                # Buscar enlace
                link = item.find('a') or titulo_elem.find('a')
                url_convocatoria = ""
                if link:
                    url_convocatoria = link.get('href', '')
                    if url_convocatoria and not url_convocatoria.startswith('http'):
                        url_convocatoria = f"https://portal.icetex.gov.co{url_convocatoria}"
                
                # Descripción
                desc_elem = item.select_one('.descripcion, .card-text, p')
                descripcion = self.clean_text(desc_elem.get_text()) if desc_elem else ""
                
                # Fechas
                fecha_elem = item.select_one('.fecha, .date')
                fecha_cierre = None
                if fecha_elem:
                    fecha_text = self.clean_text(fecha_elem.get_text())
                    fecha_cierre = self.extract_date(fecha_text)
                
                hash_content = self.create_hash(f"{titulo}{url_convocatoria}")
                
                convocatoria = {
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'url': url_convocatoria,
                    'fecha_cierre': fecha_cierre,
                    'estado': 'abierta',
                    'hash_contenido': hash_content,
                    'fuente': 'ICETEX'
                }
                
                convocatorias.append(convocatoria)
                
            except Exception as e:
                logger.error(f"Error extrayendo convocatoria ICETEX: {e}")
                continue
        
        return convocatorias
