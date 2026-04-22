"""
API REST del sistema
"""

from fastapi import APIRouter
from app.api import convocatorias, lineas, fuentes, alertas

router = APIRouter()

router.include_router(convocatorias.router, prefix="/convocatorias", tags=["convocatorias"])
router.include_router(lineas.router, prefix="/lineas", tags=["lineas"])
router.include_router(fuentes.router, prefix="/fuentes", tags=["fuentes"])
router.include_router(alertas.router, prefix="/alertas", tags=["alertas"])
