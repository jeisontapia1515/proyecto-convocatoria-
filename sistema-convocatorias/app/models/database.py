"""
Modelos de base de datos con SQLAlchemy
"""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import json

Base = declarative_base()


# Tabla de asociación muchos a muchos
convocatoria_linea_association = Table(
    'convocatoria_linea',
    Base.metadata,
    Column('convocatoria_id', Integer, ForeignKey('convocatorias.id'), primary_key=True),
    Column('linea_id', Integer, ForeignKey('lineas_investigacion.id'), primary_key=True),
    Column('puntuacion', Float, default=0.0)
)


class LineaInvestigacion(Base):
    """
    Línea de investigación de la institución
    """
    __tablename__ = 'lineas_investigacion'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False, unique=True)
    descripcion = Column(Text)
    palabras_clave = Column(Text)  # JSON array
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    convocatorias = relationship(
        "Convocatoria",
        secondary=convocatoria_linea_association,
        back_populates="lineas"
    )
    
    def get_palabras_clave(self):
        """Retorna lista de palabras clave"""
        if not self.palabras_clave:
            return []
        try:
            return json.loads(self.palabras_clave)
        except:
            return self.palabras_clave.split(',')
    
    def set_palabras_clave(self, palabras: list):
        """Guarda lista de palabras clave como JSON"""
        self.palabras_clave = json.dumps(palabras, ensure_ascii=False)


class Fuente(Base):
    """
    Fuente de convocatorias (página web, API, etc.)
    """
    __tablename__ = 'fuentes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
    tipo_scraping = Column(String(50), default='html')  # html, api, selenium
    selectores = Column(Text)  # JSON con selectores CSS/XPath
    activa = Column(Boolean, default=True)
    ultima_revision = Column(DateTime)
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    # Relaciones
    convocatorias = relationship("Convocatoria", back_populates="fuente")
    
    def get_selectores(self):
        """Retorna diccionario de selectores"""
        if not self.selectores:
            return {}
        try:
            return json.loads(self.selectores)
        except:
            return {}
    
    def set_selectores(self, selectores: dict):
        """Guarda selectores como JSON"""
        self.selectores = json.dumps(selectores, ensure_ascii=False)


class Convocatoria(Base):
    """
    Convocatoria de investigación
    """
    __tablename__ = 'convocatorias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fuente_id = Column(Integer, ForeignKey('fuentes.id'))
    titulo = Column(String(500), nullable=False)
    descripcion = Column(Text)
    url = Column(String(1000))
    fecha_apertura = Column(Date)
    fecha_cierre = Column(Date)
    monto_disponible = Column(String(200))
    requisitos = Column(Text)
    estado = Column(String(50), default='abierta')  # abierta, cerrada, proximamente
    puntuacion_relevancia = Column(Float, default=0.0)
    hash_contenido = Column(String(64))  # Para detectar duplicados
    fecha_extraccion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    notificada = Column(Boolean, default=False)
    
    # Relaciones
    fuente = relationship("Fuente", back_populates="convocatorias")
    lineas = relationship(
        "LineaInvestigacion",
        secondary=convocatoria_linea_association,
        back_populates="convocatorias"
    )
    
    def esta_activa(self):
        """Verifica si la convocatoria está activa"""
        if not self.fecha_cierre:
            return self.estado == 'abierta'
        return self.fecha_cierre >= datetime.now().date() and self.estado == 'abierta'
    
    def dias_restantes(self):
        """Retorna días restantes hasta el cierre"""
        if not self.fecha_cierre:
            return None
        delta = self.fecha_cierre - datetime.now().date()
        return delta.days if delta.days >= 0 else 0


class Alerta(Base):
    """
    Configuración de alertas por email
    """
    __tablename__ = 'alertas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), nullable=False)
    frecuencia = Column(String(50), default='diaria')  # inmediata, diaria, semanal
    lineas_interes = Column(Text)  # JSON array de IDs de líneas
    umbral_relevancia = Column(Float, default=50.0)
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    ultima_notificacion = Column(DateTime)
    
    def get_lineas_interes(self):
        """Retorna lista de IDs de líneas de interés"""
        if not self.lineas_interes:
            return []
        try:
            return json.loads(self.lineas_interes)
        except:
            return []
    
    def set_lineas_interes(self, lineas: list):
        """Guarda lista de líneas como JSON"""
        self.lineas_interes = json.dumps(lineas)


class HistorialScraping(Base):
    """
    Registro de ejecuciones de scraping
    """
    __tablename__ = 'historial_scraping'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fuente_id = Column(Integer, ForeignKey('fuentes.id'))
    fecha_inicio = Column(DateTime, default=datetime.now)
    fecha_fin = Column(DateTime)
    convocatorias_encontradas = Column(Integer, default=0)
    convocatorias_nuevas = Column(Integer, default=0)
    estado = Column(String(50))  # exitoso, error, parcial
    mensaje_error = Column(Text)
    
    # Relación
    fuente = relationship("Fuente")
