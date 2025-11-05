"""
Supabase client module - Maneja la conexión y dependencias de Supabase.

Este módulo proporciona el cliente de Supabase y el tipo de dependencia
para inyección en los endpoints de FastAPI.
"""

from typing import Annotated
from fastapi import Depends
from supabase import create_client, Client
from config.settings import settings


# Cliente de Supabase (Singleton)
_supabase_client: Client = None


def get_supabase_client() -> Client:
    """
    Obtiene o crea el cliente de Supabase.

    Implementa el patrón Singleton para reutilizar la misma conexión.

    Returns:
        Client: Instancia del cliente de Supabase
    """
    global _supabase_client

    if _supabase_client is None:
        _supabase_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )

    return _supabase_client


def get_supabase() -> Client:
    """
    Función de dependencia para FastAPI.

    Retorna el cliente de Supabase para usar en los endpoints.

    Returns:
        Client: Cliente de Supabase
    """
    return get_supabase_client()


# Tipo reutilizable para inyección de dependencias
# Uso: db: SupabaseDependency
SupabaseDependency = Annotated[Client, Depends(get_supabase)]


# Alias para mantener compatibilidad (puedes usar cualquiera de los dos)
DbDependency = SupabaseDependency
