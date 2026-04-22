"""
Configuración de la aplicación
"""

from pydantic_settings import BaseSettings
from pydantic import EmailStr, Field
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    Configuración de la aplicación desde variables de entorno
    """
    
    # Base de datos
    DATABASE_PATH: str = Field(default="database/convocatorias.db")
    
    # Email
    SMTP_SERVER: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USERNAME: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    EMAIL_FROM: str = Field(default="")
    EMAIL_TO: str = Field(default="")
    
    # Scraping
    SCRAPING_INTERVAL: int = Field(default=6)  # horas
    MAX_WORKERS: int = Field(default=5)
    REQUEST_TIMEOUT: int = Field(default=30)
    USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    
    # Filtrado
    MIN_RELEVANCE_SCORE: float = Field(default=30.0)
    KEYWORD_WEIGHT: float = Field(default=0.4)
    SEMANTIC_WEIGHT: float = Field(default=0.3)
    ENTITY_WEIGHT: float = Field(default=0.2)
    FRESHNESS_WEIGHT: float = Field(default=0.1)
    
    # Notificaciones
    INSTANT_NOTIFICATION_THRESHOLD: float = Field(default=80.0)
    WEEKLY_REPORT_DAY: str = Field(default="0")
    WEEKLY_REPORT_HOUR: int = Field(default=9)
    
    # Logs
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE_PATH: str = Field(default="logs/app.log")
    LOG_MAX_BYTES: int = Field(default=10485760)  # 10MB
    LOG_BACKUP_COUNT: int = Field(default=5)
    
    # Servidor
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=False)
    
    # Seguridad
    SECRET_KEY: str = Field(default="change-this-secret-key")
    
    # Proxy (opcional)
    HTTP_PROXY: str = Field(default="")
    HTTPS_PROXY: str = Field(default="")
    
    # Selenium
    SELENIUM_HEADLESS: bool = Field(default=True)
    CHROME_DRIVER_PATH: str = Field(default="")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def email_to_list(self) -> List[str]:
        """Convierte EMAIL_TO en lista"""
        if not self.EMAIL_TO:
            return []
        return [email.strip() for email in self.EMAIL_TO.split(",")]
    
    @property
    def database_url(self) -> str:
        """URL de conexión a la base de datos"""
        return f"sqlite:///{self.DATABASE_PATH}"
    
    @property
    def proxies(self) -> dict:
        """Configuración de proxies"""
        proxies = {}
        if self.HTTP_PROXY:
            proxies["http"] = self.HTTP_PROXY
        if self.HTTPS_PROXY:
            proxies["https"] = self.HTTPS_PROXY
        return proxies


# Crear instancia global de settings
settings = Settings()

# Asegurar que existen los directorios necesarios
BASE_DIR = Path(__file__).parent.parent
for directory in ["database", "logs", "config"]:
    dir_path = BASE_DIR / directory
    dir_path.mkdir(exist_ok=True)
