
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scrapers.nuevas_convocatorias_scraper import FondoCaldasScraper

async def main():
    scraper = FondoCaldasScraper()
    scraper.extract_convocatorias()

if __name__ == "__main__":
    asyncio.run(main())
