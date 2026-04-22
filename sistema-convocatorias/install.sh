#!/bin/bash
# Script de instalación automática para Linux/Mac

echo "==================================="
echo "Sistema de Convocatorias - Instalación"
echo "==================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Por favor instálalo primero."
    exit 1
fi

echo "✅ Python 3 encontrado"

# Crear entorno virtual
echo "Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Descargar modelo de spaCy
echo "Descargando modelo de lenguaje español..."
python -m spacy download es_core_news_md

# Copiar archivo de configuración
if [ ! -f .env ]; then
    echo "Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  Por favor edita el archivo .env con tus configuraciones"
fi

# Inicializar base de datos
echo "Inicializando base de datos..."
python scripts/init_db.py

echo ""
echo "==================================="
echo "✅ Instalación completada!"
echo "==================================="
echo ""
echo "Pasos siguientes:"
echo "1. Edita el archivo .env con tus configuraciones"
echo "2. Activa el entorno virtual: source venv/bin/activate"
echo "3. Ejecuta la aplicación: python main.py"
echo ""
echo "La aplicación estará disponible en: http://localhost:8000"
echo "==================================="
