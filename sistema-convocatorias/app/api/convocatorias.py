"""
Endpoints de convocatorias
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.connection import get_db
from app.models import Convocatoria, LineaInvestigacion
from datetime import datetime

router = APIRouter()


@router.get("/")
def listar_convocatorias(
    estado: Optional[str] = None,
    linea_id: Optional[int] = None,
    buscar: Optional[str] = None,
    vigentes: bool = False,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Lista convocatorias con filtros"""
    query = db.query(Convocatoria)
    
    if vigentes:
        today = datetime.now().date()
        query = query.filter(
            (Convocatoria.fecha_cierre >= today) | 
            (Convocatoria.fecha_cierre == None)
        )
    
    if estado:
        query = query.filter(Convocatoria.estado == estado)
    
    if linea_id:
        query = query.join(Convocatoria.lineas).filter(
            LineaInvestigacion.id == linea_id
        )
    
    if buscar:
        query = query.filter(
            Convocatoria.titulo.contains(buscar) |
            Convocatoria.descripcion.contains(buscar)
        )
    
    total = query.count()
    convocatorias = query.order_by(
        Convocatoria.puntuacion_relevancia.desc()
    ).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [
            {
                "id": c.id,
                "titulo": c.titulo,
                "descripcion": c.descripcion[:200] if c.descripcion else "",
                "url": c.url,
                "fecha_apertura": c.fecha_apertura.isoformat() if c.fecha_apertura else None,
                "fecha_cierre": c.fecha_cierre.isoformat() if c.fecha_cierre else None,
                "dias_restantes": c.dias_restantes(),
                "estado": c.estado,
                "puntuacion": c.puntuacion_relevancia,
                "fuente": c.fuente.nombre if c.fuente else None
            }
            for c in convocatorias
        ]
    }


@router.get("/{convocatoria_id}")
def obtener_convocatoria(
    convocatoria_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene detalle de una convocatoria"""
    conv = db.query(Convocatoria).filter(Convocatoria.id == convocatoria_id).first()
    if not conv:
        return {"error": "No encontrada"}
    
    return {
        "id": conv.id,
        "titulo": conv.titulo,
        "descripcion": conv.descripcion,
        "url": conv.url,
        "fecha_apertura": conv.fecha_apertura.isoformat() if conv.fecha_apertura else None,
        "fecha_cierre": conv.fecha_cierre.isoformat() if conv.fecha_cierre else None,
        "dias_restantes": conv.dias_restantes(),
        "estado": conv.estado,
        "puntuacion": conv.puntuacion_relevancia,
        "fuente": conv.fuente.nombre if conv.fuente else None,
        "lineas": [
            {"id": l.id, "nombre": l.nombre}
            for l in conv.lineas
        ]
    }
