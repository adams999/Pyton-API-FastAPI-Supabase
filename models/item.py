"""
Esquemas Pydantic para la entidad Item.

Define los modelos de datos para crear, leer y manipular items.
"""

from typing import Optional
import uuid
from pydantic import BaseModel, Field
from datetime import datetime


class ItemCreate(BaseModel):
    """
    Schema para crear un nuevo Item.

    No incluye el ID ya que este es generado automáticamente por Supabase.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del item")
    description: str = Field(..., min_length=1, max_length=500, description="Descripción del item")
    price: Optional[float] = Field(None, ge=0, description="Precio del item")
    tax: Optional[float] = Field(None, ge=0, description="Impuesto aplicable")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Producto ejemplo",
                    "description": "Una descripción detallada del producto",
                    "price": 99.99,
                    "tax": 21.0
                }
            ]
        }
    }


class ItemBase(ItemCreate):
    """
    Schema base para Item con ID.

    Incluye el ID generado por Supabase.
    """
    id: uuid.UUID = Field(..., description="ID único del item")


class Item(ItemBase):
    """
    Schema completo para Item.

    Incluye todos los campos incluyendo metadata de creación.
    """
    created_at: Optional[datetime] = Field(None, description="Fecha y hora de creación")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Producto ejemplo",
                    "description": "Una descripción detallada del producto",
                    "price": 99.99,
                    "tax": 21.0,
                    "created_at": "2024-01-01T00:00:00"
                }
            ]
        }
    }
