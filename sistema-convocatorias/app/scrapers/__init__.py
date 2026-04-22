"""
Módulo de scrapers para diferentes fuentes
"""

from app.scrapers.base_scraper import BaseScraper
from app.scrapers.minciencias_scraper import (
    MincienciasScraper,
    SENAScraper,
    ICETEXScraper
)

__all__ = [
    'BaseScraper',
    'MincienciasScraper',
    'SENAScraper',
    'ICETEXScraper'
]
