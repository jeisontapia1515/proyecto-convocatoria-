"""
Configuración de logging
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.utils.config import settings


def setup_logger():
    """
    Configura el sistema de logging de la aplicación
    """
    
    # Crear directorio de logs si no existe
    log_dir = Path(settings.LOG_FILE_PATH).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para archivo con rotación
    file_handler = RotatingFileHandler(
        settings.LOG_FILE_PATH,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Configurar logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Archivo separado para errores
    error_handler = RotatingFileHandler(
        log_dir / "errors.log",
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    root_logger.addHandler(error_handler)
    
    # Archivo separado para scraping
    scraping_logger = logging.getLogger('scraping')
    scraping_handler = RotatingFileHandler(
        log_dir / "scraping.log",
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    scraping_handler.setFormatter(formatter)
    scraping_logger.addHandler(scraping_handler)
    
    # Reducir verbosidad de librerías externas
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    logging.info("Sistema de logging configurado correctamente")
