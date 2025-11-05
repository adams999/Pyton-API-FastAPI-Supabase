"""
Database package - Maneja todas las conexiones a bases de datos.

Actualmente soporta:
- Supabase: Cliente y dependencias para PostgreSQL a través de Supabase

Para agregar más bases de datos en el futuro, crea módulos adicionales aquí:
- mongodb.py
- redis.py
- etc.
"""

from .supabase import (
    get_supabase,
    get_supabase_client,
    SupabaseDependency,
    DbDependency
)

__all__ = [
    "get_supabase",
    "get_supabase_client",
    "SupabaseDependency",
    "DbDependency",
]
