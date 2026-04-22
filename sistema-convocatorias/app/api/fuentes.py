from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.connection import get_db
from app.models import Fuente

router = APIRouter()

@router.get("/")
def listar_fuentes(db: Session = Depends(get_db)):
    fuentes = db.query(Fuente).all()
    return [{"id": f.id, "nombre": f.nombre, "url": f.url, "activa": f.activa} for f in fuentes]
