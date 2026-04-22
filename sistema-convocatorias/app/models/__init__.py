"""
Modelos de base de datos
"""

from app.models.database import (
    Base,
    LineaInvestigacion,
    Fuente,
    Convocatoria,
    Alerta,
    HistorialScraping
)

__all__ = [
    'Base',
    'LineaInvestigacion',
    'Fuente',
    'Convocatoria',
    'Alerta',
    'HistorialScraping'
]
