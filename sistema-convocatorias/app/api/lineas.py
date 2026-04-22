from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.connection import get_db
from app.models import LineaInvestigacion
import json

router = APIRouter()

@router.get("/")
def listar_lineas(db: Session = Depends(get_db)):
    lineas = db.query(LineaInvestigacion).filter_by(activa=True).all()
    return [{"id": l.id, "nombre": l.nombre, "descripcion": l.descripcion} for l in lineas]

@router.post("/")
def crear_linea(nombre: str, descripcion: str, palabras_clave: str, db: Session = Depends(get_db)):
    linea = LineaInvestigacion(nombre=nombre, descripcion=descripcion)
    linea.set_palabras_clave(palabras_clave.split(','))
    db.add(linea)
    db.commit()
    return {"id": linea.id, "mensaje": "Creada"}
