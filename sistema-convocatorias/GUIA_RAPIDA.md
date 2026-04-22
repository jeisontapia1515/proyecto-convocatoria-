# Guía Rápida de Uso

## Instalación

### Linux/Mac:
```bash
chmod +x install.sh
./install.sh
```

### Windows:
```cmd
install.bat
```

## Iniciar el Sistema

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Ejecutar aplicación
python main.py
```

Acceder a: http://localhost:8000

## Configuración Inicial

### 1. Configurar Email (archivo .env)
```
SMTP_USERNAME=tu_email@gmail.com
SMTP_PASSWORD=tu_contraseña_aplicación
EMAIL_TO=destino1@universidad.edu.co,destino2@universidad.edu.co
```

### 2. Agregar Líneas de Investigación
- Ve a http://localhost:8000/admin/lineas
- Click en "Nueva Línea"
- Completa el formulario:
  - Nombre: ej. "Inteligencia Artificial"
  - Descripción: Breve descripción
  - Palabras clave: machine learning, IA, deep learning

### 3. Ejecutar Primer Scraping
```bash
python scripts/run_scraping.py
```

## Uso Diario

### Ver Dashboard
http://localhost:8000

### Buscar Convocatorias
http://localhost:8000/convocatorias

### Ver Estadísticas
http://localhost:8000/estadisticas

## Mantenimiento

### Backup Manual
```bash
python scripts/backup.py
```

### Ver Logs
```bash
tail -f logs/app.log
```

## Solución de Problemas

### Error: No se pueden enviar emails
1. Verifica credenciales en .env
2. Para Gmail: usa contraseña de aplicación

### Error: Modelo spaCy no encontrado
```bash
python -m spacy download es_core_news_md
```

### Base de datos bloqueada
```bash
# Cerrar todas las instancias
pkill -f "python main.py"
```

## Comandos Útiles

```bash
# Ejecutar scraping
python scripts/run_scraping.py

# Crear backup
python scripts/backup.py

# Reiniciar base de datos (¡CUIDADO!)
rm database/convocatorias.db
python scripts/init_db.py
```

## Contacto

Para soporte: soporte-ti@universidad.edu.co
