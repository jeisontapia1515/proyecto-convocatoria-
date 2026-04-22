# Sistema de Monitoreo Automático de Convocatorias de Investigación

Sistema automatizado para identificar, filtrar y notificar convocatorias de investigación a nivel nacional según líneas investigativas específicas.

## 🎯 Características Principales

- ✅ Monitoreo automático de múltiples fuentes nacionales
- ✅ Filtrado inteligente por líneas de investigación
- ✅ Sistema de notificaciones por email
- ✅ Dashboard web intuitivo
- ✅ 100% gratuito y open source
- ✅ Despliegue local sin dependencias externas

## 📋 Requisitos del Sistema

- Python 3.10 o superior
- 2GB RAM mínimo
- 1GB espacio en disco
- Sistema operativo: Windows/Linux/MacOS

## 🚀 Instalación Rápida

### 1. Clonar o descargar el proyecto

```bash
# Si tienes el archivo ZIP, descomprímelo
unzip sistema-convocatorias.zip
cd sistema-convocatorias
```

### 2. Crear entorno virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Descargar modelo de lenguaje español

```bash
python -m spacy download es_core_news_md
```

### 5. Inicializar base de datos

```bash
python scripts/init_db.py
```

### 6. Configurar variables de entorno

```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

Edita el archivo `.env` con tus configuraciones:

```
# Email para notificaciones
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu_email@gmail.com
SMTP_PASSWORD=tu_contraseña_app
EMAIL_FROM=tu_email@gmail.com

# Destinatarios (separados por coma)
EMAIL_TO=decanatura@universidad.edu.co,investigacion@universidad.edu.co

# Base de datos
DATABASE_PATH=database/convocatorias.db

# Configuración de scraping
SCRAPING_INTERVAL=6  # horas
MAX_WORKERS=5
```

### 7. Ejecutar la aplicación

```bash
python main.py
```

La aplicación estará disponible en:
- **Interfaz web**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:8000/admin

## 📖 Guía de Uso

### Configuración Inicial

#### 1. Agregar Líneas de Investigación

Accede a http://localhost:8000/admin/lineas y agrega tus líneas de investigación:

- **Nombre**: Nombre de la línea (ej: "Inteligencia Artificial")
- **Descripción**: Descripción detallada
- **Palabras clave**: Lista de palabras clave separadas por comas

Ejemplo:
```
Nombre: Inteligencia Artificial
Descripción: Investigación en algoritmos de aprendizaje automático, redes neuronales y aplicaciones de IA
Palabras clave: inteligencia artificial, machine learning, deep learning, redes neuronales, IA, aprendizaje automático, visión computacional
```

#### 2. Configurar Fuentes

Las fuentes principales ya están preconfiguradas, pero puedes agregar más en:
http://localhost:8000/admin/fuentes

Fuentes incluidas por defecto:
- Minciencias
- SENA
- ICETEX
- Ministerio de Educación
- Colciencias

#### 3. Configurar Notificaciones

En http://localhost:8000/admin/alertas puedes:
- Agregar correos electrónicos
- Seleccionar líneas de interés
- Configurar frecuencia (inmediata, diaria, semanal)

### Uso Diario

#### Dashboard Principal

El dashboard muestra:
- Convocatorias activas
- Próximas a cerrar
- Nuevas convocatorias
- Estadísticas generales

#### Filtrar Convocatorias

Usa los filtros para:
- Buscar por texto
- Filtrar por línea de investigación
- Filtrar por estado (abierta/cerrada/próximamente)
- Ordenar por relevancia o fecha

#### Exportar Resultados

Puedes exportar convocatorias a:
- Excel (.xlsx)
- PDF
- CSV

## 🔧 Configuración Avanzada

### Agregar Nuevas Fuentes

Edita el archivo `config/fuentes.json` para agregar nuevas fuentes:

```json
{
  "nombre": "Nueva Fuente",
  "url": "https://ejemplo.com/convocatorias",
  "tipo_scraping": "html",
  "selectores": {
    "contenedor": "div.convocatoria",
    "titulo": "h2.titulo",
    "descripcion": "p.descripcion",
    "fecha_cierre": "span.fecha",
    "url": "a.ver-mas"
  },
  "activa": true
}
```

### Personalizar Algoritmo de Filtrado

Edita `app/services/filter_service.py` para ajustar:
- Pesos de relevancia
- Umbrales de coincidencia
- Criterios de filtrado

### Programar Tareas

Edita `config/scheduler.json` para configurar:

```json
{
  "scraping_interval": 6,  # horas
  "cleanup_interval": 24,  # horas
  "weekly_report_day": "monday",
  "weekly_report_hour": 9
}
```

## 🛠️ Scripts Útiles

### Ejecutar Scraping Manual

```bash
python scripts/run_scraping.py
```

### Generar Reporte

```bash
python scripts/generate_report.py --periodo mensual
```

### Limpiar Base de Datos

```bash
python scripts/cleanup.py --antiguedad 180  # días
```

### Backup de Base de Datos

```bash
python scripts/backup.py
```

## 📊 Monitoreo y Logs

Los logs se guardan en el directorio `logs/`:

- `app.log` - Log general de la aplicación
- `scraping.log` - Log de actividades de scraping
- `errors.log` - Log de errores

Ver logs en tiempo real:

```bash
tail -f logs/app.log
```

## 🔍 Solución de Problemas

### Error: No se pueden enviar emails

**Solución**: Si usas Gmail, debes:
1. Habilitar "Verificación en 2 pasos"
2. Generar una "Contraseña de aplicación"
3. Usar esa contraseña en `SMTP_PASSWORD`

[Guía de Google](https://support.google.com/accounts/answer/185833)

### Error: Scraper no encuentra elementos

**Solución**: Las páginas web cambian. Actualiza los selectores en `config/fuentes.json`

### Base de datos bloqueada

**Solución**: Cierra otras instancias de la aplicación

```bash
# Linux/Mac
pkill -f "python main.py"

# Windows
taskkill /F /IM python.exe
```

### Modelo de spaCy no encontrado

**Solución**: Reinstalar el modelo

```bash
python -m spacy download es_core_news_md --force
```

## 📁 Estructura del Proyecto

```
sistema-convocatorias/
├── app/
│   ├── api/                 # Endpoints de la API
│   ├── models/              # Modelos de base de datos
│   ├── scrapers/            # Web scrapers
│   ├── services/            # Lógica de negocio
│   └── utils/               # Utilidades
├── config/                  # Archivos de configuración
├── database/                # Base de datos SQLite
├── logs/                    # Archivos de log
├── scripts/                 # Scripts de utilidad
├── static/                  # CSS, JS, imágenes
├── templates/               # Plantillas HTML
├── tests/                   # Tests unitarios
├── .env.example            # Ejemplo de variables de entorno
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias Python
└── README.md              # Esta documentación
```

## 🧪 Tests

Ejecutar tests:

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_scrapers.py
pytest tests/test_filter.py

# Con cobertura
pytest --cov=app tests/
```

## 🤝 Contribuciones

Este es un proyecto interno, pero puedes:

1. Reportar bugs en el sistema de tickets interno
2. Sugerir mejoras al equipo de desarrollo
3. Documentar casos de uso

## 📝 Licencia

Uso interno - Universidad [Nombre]
Todos los derechos reservados.

## 📧 Contacto y Soporte

- **Soporte técnico**: soporte-ti@universidad.edu.co
- **Decanatura de Investigación**: investigacion@universidad.edu.co

## 🔄 Actualizaciones

### Versión 1.0.0 (Actual)
- Sistema base de scraping
- Filtrado por líneas de investigación
- Dashboard web
- Sistema de notificaciones

### Próximas versiones
- Integración con APIs oficiales
- Machine Learning para mejor filtrado
- Aplicación móvil
- Integración con calendario institucional

## 📚 Recursos Adicionales

- [Documentación completa](docs/documentacion.pdf)
- [Video tutorial](docs/tutorial.mp4)
- [Manual de usuario](docs/manual-usuario.pdf)
- [Guía de administrador](docs/manual-admin.pdf)

## ⚙️ Mantenimiento

### Tareas Automáticas Programadas

- **Cada hora**: Revisar fuentes prioritarias (Minciencias)
- **Cada 6 horas**: Revisar todas las fuentes
- **Diario a las 6 AM**: Limpiar convocatorias vencidas
- **Lunes 9 AM**: Enviar resumen semanal
- **Día 1 de cada mes**: Generar reporte mensual

### Mantenimiento Manual Recomendado

**Semanal**:
- Revisar logs de errores
- Verificar funcionamiento de scrapers
- Validar nuevas convocatorias

**Mensual**:
- Actualizar palabras clave
- Revisar fuentes inactivas
- Backup de base de datos
- Análisis de estadísticas

**Semestral**:
- Actualización de dependencias
- Optimización de base de datos
- Revisión de algoritmo de filtrado

---

**¡Sistema listo para usar! 🚀**

Si tienes preguntas, consulta la documentación completa o contacta al equipo de soporte.
