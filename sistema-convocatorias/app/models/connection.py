"""
Gestión de conexión a base de datos
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from app.models.database import Base
from app.utils.config import settings
import logging

logger = logging.getLogger(__name__)

# Crear engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # Solo para SQLite
    echo=settings.DEBUG
)

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Inicializa la base de datos creando todas las tablas
    """
    logger.info("Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Base de datos inicializada correctamente")


def get_db() -> Session:
    """
    Dependency para obtener sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager para usar fuera de FastAPI
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error en transacción de base de datos: {e}")
        raise
    finally:
        db.close()
