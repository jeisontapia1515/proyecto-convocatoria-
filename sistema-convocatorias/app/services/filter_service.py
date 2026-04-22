"""
Servicio de filtrado inteligente de convocatorias
"""

import importlib.util
import sys

# Importación lazy de spacy para manejar incompatibilidades
spacy = None
SPACY_AVAILABLE = False
try:
    spec = importlib.util.find_spec("spacy")
    if spec is not None:
        spacy = importlib.import_module("spacy")
        # Verificar que spacy funcione correctamente
        _ = spacy.load("es_core_news_md")
        SPACY_AVAILABLE = True
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ spaCy no disponible: {e}. Las funciones de NLP avanzadas están deshabilitadas.")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from app.utils.config import settings

logger = logging.getLogger(__name__)

# Cargar modelo de spaCy para español (solo si está disponible)
nlp = None
if SPACY_AVAILABLE:
    try:
        nlp = spacy.load("es_core_news_md")
        logger.info("✅ Modelo de spaCy cargado correctamente")
    except Exception as e:
        logger.warning(f"⚠️ Error cargando modelo de spaCy: {e}")


class FilterService:
    """
    Servicio para filtrar y puntuar convocatorias según relevancia
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english'
        )
    
    def calcular_relevancia(
        self,
        convocatoria: Dict,
        linea_investigacion: Dict
    ) -> float:
        """
        Calcula score de relevancia (0-100) entre convocatoria y línea
        
        Args:
            convocatoria: Dict con datos de convocatoria
            linea_investigacion: Dict con datos de línea de investigación
        
        Returns:
            float: Score de relevancia (0-100)
        """
        score = 0.0
        
        # Texto completo de la convocatoria
        texto_convocatoria = f"{convocatoria.get('titulo', '')} {convocatoria.get('descripcion', '')}"
        texto_convocatoria = texto_convocatoria.lower()
        
        # 1. Coincidencia de palabras clave (40%)
        keyword_score = self._calcular_keyword_score(
            texto_convocatoria,
            linea_investigacion.get('palabras_clave', [])
        )
        score += keyword_score * settings.KEYWORD_WEIGHT * 100
        
        # 2. Similitud semántica (30%)
        if nlp:
            semantic_score = self._calcular_similitud_semantica(
                texto_convocatoria,
                linea_investigacion.get('descripcion', '')
            )
            score += semantic_score * settings.SEMANTIC_WEIGHT * 100
        
        # 3. Análisis de entidades (20%)
        if nlp:
            entity_score = self._analizar_entidades(
                texto_convocatoria,
                linea_investigacion
            )
            score += entity_score * settings.ENTITY_WEIGHT * 100
        
        # 4. Frescura de la convocatoria (10%)
        freshness_score = self._calcular_frescura(
            convocatoria.get('fecha_extraccion')
        )
        score += freshness_score * settings.FRESHNESS_WEIGHT * 100
        
        return min(100.0, max(0.0, score))
    
    def _calcular_keyword_score(
        self,
        texto: str,
        palabras_clave: List[str]
    ) -> float:
        """
        Calcula score basado en coincidencia de palabras clave
        """
        if not palabras_clave:
            return 0.0
        
        texto_lower = texto.lower()
        coincidencias = 0
        
        for palabra in palabras_clave:
            if isinstance(palabra, str):
                palabra_lower = palabra.lower().strip()
                if palabra_lower in texto_lower:
                    coincidencias += 1
        
        return min(1.0, coincidencias / len(palabras_clave))
    
    def _calcular_similitud_semantica(
        self,
        texto1: str,
        texto2: str
    ) -> float:
        """
        Calcula similitud semántica usando vectores de spaCy
        """
        if not texto1 or not texto2:
            return 0.0
        
        try:
            doc1 = nlp(texto1[:1000000])  # Limitar tamaño
            doc2 = nlp(texto2[:1000000])
            
            return doc1.similarity(doc2)
        except Exception as e:
            logger.error(f"Error calculando similitud semántica: {e}")
            return 0.0
    
    def _analizar_entidades(
        self,
        texto: str,
        linea_investigacion: Dict
    ) -> float:
        """
        Analiza entidades nombradas en el texto
        """
        try:
            doc = nlp(texto[:1000000])
            
            # Extraer entidades
            entidades = [ent.text.lower() for ent in doc.ents]
            
            # Buscar coincidencias con palabras clave de la línea
            palabras_clave = linea_investigacion.get('palabras_clave', [])
            if not palabras_clave:
                return 0.0
            
            coincidencias = 0
            for palabra in palabras_clave:
                if isinstance(palabra, str):
                    palabra_lower = palabra.lower()
                    if any(palabra_lower in ent for ent in entidades):
                        coincidencias += 1
            
            return min(1.0, coincidencias / len(palabras_clave))
        
        except Exception as e:
            logger.error(f"Error analizando entidades: {e}")
            return 0.0
    
    def _calcular_frescura(self, fecha_extraccion) -> float:
        """
        Calcula score basado en qué tan reciente es la convocatoria
        """
        if not fecha_extraccion:
            return 0.5
        
        if isinstance(fecha_extraccion, str):
            try:
                fecha_extraccion = datetime.fromisoformat(fecha_extraccion)
            except:
                return 0.5
        
        dias_transcurridos = (datetime.now() - fecha_extraccion).days
        
        if dias_transcurridos <= 7:
            return 1.0
        elif dias_transcurridos <= 30:
            return 0.7
        elif dias_transcurridos <= 90:
            return 0.4
        else:
            return 0.2
    
    def filtrar_convocatorias(
        self,
        convocatorias: List[Dict],
        lineas_investigacion: List[Dict],
        umbral_minimo: float = None
    ) -> List[Tuple[Dict, List[Tuple[Dict, float]]]]:
        """
        Filtra convocatorias por líneas de investigación
        
        Args:
            convocatorias: Lista de convocatorias
            lineas_investigacion: Lista de líneas de investigación
            umbral_minimo: Score mínimo de relevancia (usa settings si None)
        
        Returns:
            Lista de tuplas (convocatoria, [(linea, score)])
        """
        if umbral_minimo is None:
            umbral_minimo = settings.MIN_RELEVANCE_SCORE
        
        resultados = []
        
        for convocatoria in convocatorias:
            matches = []
            
            for linea in lineas_investigacion:
                score = self.calcular_relevancia(convocatoria, linea)
                
                if score >= umbral_minimo:
                    matches.append((linea, score))
            
            # Ordenar matches por score descendente
            matches.sort(key=lambda x: x[1], reverse=True)
            
            if matches:
                # Score general es el máximo de todos los matches
                convocatoria['puntuacion_relevancia'] = matches[0][1]
                resultados.append((convocatoria, matches))
        
        # Ordenar resultados por relevancia
        resultados.sort(key=lambda x: x[0]['puntuacion_relevancia'], reverse=True)
        
        return resultados
