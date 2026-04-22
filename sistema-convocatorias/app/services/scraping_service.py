"""
Servicio principal de scraping
"""

import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from app.scrapers import MincienciasScraper, SENAScraper, ICETEXScraper
from app.models.connection import get_db_context
from app.models import Convocatoria, Fuente, HistorialScraping
from app.utils.config import settings

logger = logging.getLogger('scraping')


class ScrapingService:
    """
    Coordina el scraping de todas las fuentes
    """
    
    def __init__(self):
        self.scrapers = {
            'Minciencias': MincienciasScraper(),
            'SENA': SENAScraper(),
            'ICETEX': ICETEXScraper()
        }
    
    def ejecutar_scraping_completo(self):
        """
        Ejecuta scraping de todas las fuentes activas
        """
        logger.info("=== Iniciando scraping completo ===")
        
        with ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
            futures = []
            for nombre, scraper in self.scrapers.items():
                future = executor.submit(self.ejecutar_scraper, nombre, scraper)
                futures.append(future)
            
            # Esperar a que terminen todos
            for future in futures:
                future.result()
        
        logger.info("=== Scraping completo finalizado ===")
    
    def ejecutar_scraper(self, nombre, scraper):
        """
        Ejecuta un scraper individual
        """
        try:
            logger.info(f"Ejecutando scraper: {nombre}")
            convocatorias = scraper.run()
            
            # Guardar en base de datos
            self.guardar_convocatorias(nombre, convocatorias)
            
        except Exception as e:
            logger.error(f"Error en scraper {nombre}: {e}", exc_info=True)
    
    def guardar_convocatorias(self, fuente_nombre, convocatorias):
        """
        Guarda convocatorias en la base de datos
        """
        with get_db_context() as db:
            # Buscar o crear fuente
            fuente = db.query(Fuente).filter_by(nombre=fuente_nombre).first()
            if not fuente:
                fuente = Fuente(nombre=fuente_nombre, url="", tipo_scraping="html")
                db.add(fuente)
                db.commit()
            
            nuevas = 0
            for conv_data in convocatorias:
                # Verificar si ya existe
                existe = db.query(Convocatoria).filter_by(
                    hash_contenido=conv_data.get('hash_contenido')
                ).first()
                
                if not existe:
                    conv = Convocatoria(
                        fuente_id=fuente.id,
                        titulo=conv_data.get('titulo'),
                        descripcion=conv_data.get('descripcion'),
                        url=conv_data.get('url'),
                        fecha_apertura=conv_data.get('fecha_apertura'),
                        fecha_cierre=conv_data.get('fecha_cierre'),
                        estado=conv_data.get('estado', 'abierta'),
                        hash_contenido=conv_data.get('hash_contenido')
                    )
                    db.add(conv)
                    nuevas += 1
                else:
                    # Actualizar información existente
                    if conv_data.get('fecha_cierre'):
                        existe.fecha_cierre = conv_data.get('fecha_cierre')
                    if conv_data.get('fecha_apertura'):
                        existe.fecha_apertura = conv_data.get('fecha_apertura')
                    if conv_data.get('estado'):
                        existe.estado = conv_data.get('estado')
                    if conv_data.get('descripcion'):
                        existe.descripcion = conv_data.get('descripcion')
            
            db.commit()
            logger.info(f"{nuevas} nuevas convocatorias de {fuente_nombre}")
