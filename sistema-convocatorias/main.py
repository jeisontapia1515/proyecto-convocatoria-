"""
Sistema de Monitoreo Automático de Convocatorias de Investigación
Punto de entrada principal de la aplicación
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import logging
from pathlib import Path

from app.api import router as api_router
from app.services.scheduler_service import SchedulerService
from app.utils.logger import setup_logger
from app.utils.config import settings

# Configurar logging
setup_logger()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación
    """
    logger.info("🚀 Iniciando Sistema de Convocatorias...")
    
    # Iniciar scheduler para tareas automáticas
    scheduler = SchedulerService()
    scheduler.start()
    logger.info("✅ Scheduler iniciado correctamente")
    
    yield
    
    # Cleanup
    logger.info("🛑 Deteniendo aplicación...")
    scheduler.stop()
    logger.info("✅ Aplicación detenida correctamente")


# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Convocatorias",
    description="Sistema automatizado de monitoreo de convocatorias de investigación",
    version="1.0.0",
    lifespan=lifespan
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Incluir routers de la API
app.include_router(api_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Página principal - Dashboard
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    """
    Panel de administración
    """
    return templates.TemplateResponse(
        "admin.html",
        {"request": request}
    )


@app.get("/admin/lineas", response_class=HTMLResponse)
async def admin_lineas(request: Request):
    """
    Gestión de líneas de investigación
    """
    return templates.TemplateResponse(
        "admin_lineas.html",
        {"request": request}
    )


@app.get("/admin/fuentes", response_class=HTMLResponse)
async def admin_fuentes(request: Request):
    """
    Gestión de fuentes
    """
    return templates.TemplateResponse(
        "admin_fuentes.html",
        {"request": request}
    )


@app.get("/admin/alertas", response_class=HTMLResponse)
async def admin_alertas(request: Request):
    """
    Gestión de alertas
    """
    return templates.TemplateResponse(
        "admin_alertas.html",
        {"request": request}
    )


@app.get("/convocatorias", response_class=HTMLResponse)
async def convocatorias(request: Request):
    """
    Listado de convocatorias
    """
    return templates.TemplateResponse(
        "convocatorias.html",
        {"request": request}
    )


@app.get("/estadisticas", response_class=HTMLResponse)
async def estadisticas(request: Request):
    """
    Estadísticas y reportes
    """
    return templates.TemplateResponse(
        "estadisticas.html",
        {"request": request}
    )


@app.get("/health")
async def health_check():
    """
    Endpoint de health check
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Sistema de Convocatorias"
    }


if __name__ == "__main__":
    logger.info(f"🌐 Servidor iniciando en http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📚 Documentación disponible en http://{settings.HOST}:{settings.PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
