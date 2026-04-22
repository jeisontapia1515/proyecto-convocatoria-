@echo off
REM Script de instalación automática para Windows

echo ===================================
echo Sistema de Convocatorias - Instalación
echo ===================================

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no encontrado
    pause
    exit /b 1
)

echo Python encontrado

REM Crear entorno virtual
echo Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Descargar modelo de spaCy
echo Descargando modelo de lenguaje español...
python -m spacy download es_core_news_md

REM Copiar archivo de configuración
if not exist .env (
    echo Creando archivo .env...
    copy .env.example .env
    echo Por favor edita el archivo .env con tus configuraciones
)

REM Inicializar base de datos
echo Inicializando base de datos...
python scripts\init_db.py

echo.
echo ===================================
echo Instalación completada!
echo ===================================
echo.
echo Pasos siguientes:
echo 1. Edita el archivo .env con tus configuraciones
echo 2. Activa el entorno virtual: venv\Scripts\activate.bat
echo 3. Ejecuta la aplicación: python main.py
echo.
echo La aplicación estará disponible en: http://localhost:8000
echo ===================================
pause
