#!/usr/bin/env python3
"""
Script para inicializar la base de datos
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.connection import init_db, get_db_context
from app.models import LineaInvestigacion, Fuente
import json

def crear_datos_iniciales():
    """Crea datos iniciales en la base de datos"""
    
    with get_db_context() as db:
        # Crear líneas de investigación de ejemplo
        if db.query(LineaInvestigacion).count() == 0:
            lineas_ejemplo = [
                {
                    "nombre": "Inteligencia Artificial y Machine Learning",
                    "descripcion": "Investigación en algoritmos de aprendizaje automático, redes neuronales y aplicaciones de IA",
                    "palabras_clave": ["inteligencia artificial", "machine learning", "deep learning", "redes neuronales", "IA", "aprendizaje automático"]
                },
                {
                    "nombre": "Biotecnología y Biomedicina",
                    "descripcion": "Investigación en ingeniería genética, desarrollo de fármacos y aplicaciones médicas",
                    "palabras_clave": ["biotecnología", "biomedicina", "ingeniería genética", "bioinformática", "farmacología"]
                },
                {
                    "nombre": "Energías Renovables",
                    "descripcion": "Investigación en energía solar, eólica y otras fuentes renovables",
                    "palabras_clave": ["energía solar", "energía eólica", "renovables", "sostenibilidad", "energía limpia"]
                }
            ]
            
            for linea_data in lineas_ejemplo:
                linea = LineaInvestigacion(
                    nombre=linea_data["nombre"],
                    descripcion=linea_data["descripcion"]
                )
                linea.set_palabras_clave(linea_data["palabras_clave"])
                db.add(linea)
            
            print("✅ Líneas de investigación creadas")
        
        # Crear fuentes
        if db.query(Fuente).count() == 0:
            fuentes = [
                {"nombre": "Minciencias", "url": "https://minciencias.gov.co/convocatorias", "tipo_scraping": "html"},
                {"nombre": "SENA", "url": "https://www.sena.edu.co/es-co/sennova/Paginas/convocatorias.aspx", "tipo_scraping": "html"},
                {"nombre": "ICETEX", "url": "https://portal.icetex.gov.co/Portal/home/convocatorias", "tipo_scraping": "html"},
            ]
            
            for fuente_data in fuentes:
                fuente = Fuente(**fuente_data)
                db.add(fuente)
            
            print("✅ Fuentes creadas")
        
        db.commit()

if __name__ == "__main__":
    print("Inicializando base de datos...")
    init_db()
    print("✅ Base de datos inicializada")
    
    print("\nCreando datos iniciales...")
    crear_datos_iniciales()
    print("✅ Datos iniciales creados")
    
    print("\n🎉 ¡Sistema listo para usar!")
