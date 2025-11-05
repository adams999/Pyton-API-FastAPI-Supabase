"""
Settings module - Configuración centralizada de la aplicación usando Pydantic Settings.

Este módulo maneja todas las variables de entorno y configuraciones de la aplicación.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Las variables se cargan automáticamente desde el archivo .env
    """

    # Configuración de la aplicación
    APP_NAME: str = "FastAPI + Supabase API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Configuración de Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Configuración de la API
    API_PREFIX: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Instancia global de settings (Singleton pattern)
settings = Settings()
