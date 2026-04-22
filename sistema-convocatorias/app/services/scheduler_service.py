"""
Servicio de programación de tareas automáticas
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from app.services.scraping_service import ScrapingService
from app.utils.config import settings

logger = logging.getLogger(__name__)


class SchedulerService:
    """
    Gestiona tareas programadas
    """
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scraping_service = ScrapingService()
    
    def start(self):
        """Inicia el scheduler"""
        # Scraping cada X horas
        self.scheduler.add_job(
            self.scraping_service.ejecutar_scraping_completo,
            'interval',
            hours=settings.SCRAPING_INTERVAL,
            id='scraping_job'
        )
        
        # Reporte semanal
        day = settings.WEEKLY_REPORT_DAY
        if day == 'monday': day = 'mon'
        
        self.scheduler.add_job(
            self.generar_reporte_semanal,
            CronTrigger(
                day_of_week=day,
                hour=settings.WEEKLY_REPORT_HOUR
            ),
            id='weekly_report'
        )
        
        # Limpieza diaria
        self.scheduler.add_job(
            self.limpiar_convocatorias_antiguas,
            'cron',
            hour=6,
            id='cleanup_job'
        )
        
        self.scheduler.start()
        logger.info("Scheduler iniciado")
    
    def stop(self):
        """Detiene el scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler detenido")
    
    def generar_reporte_semanal(self):
        """Genera y envía reporte semanal"""
        logger.info("Generando reporte semanal...")
        # Implementar lógica de reporte
    
    def limpiar_convocatorias_antiguas(self):
        """Limpia convocatorias antiguas"""
        logger.info("Limpiando convocatorias antiguas...")
        # Implementar lógica de limpieza
