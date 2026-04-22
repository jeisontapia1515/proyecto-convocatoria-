from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.connection import get_db
from app.models import Alerta

router = APIRouter()

@router.get("/")
def listar_alertas(db: Session = Depends(get_db)):
    alertas = db.query(Alerta).all()
    return [{"id": a.id, "email": a.email, "frecuencia": a.frecuencia} for a in alertas]
