#!/usr/bin/env python3
"""
Ejecutar scraping manualmente
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.scraping_service import ScrapingService
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("Ejecutando scraping...")
    service = ScrapingService()
    service.ejecutar_scraping_completo()
    print("✅ Scraping completado")
