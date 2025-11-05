from fastapi import HTTPException
from db import get_supabase_client
from models import Item, ItemBase, ItemCreate
import uuid


class ItemService:
    """Servicio que contiene la lógica de negocio para items"""

    @staticmethod
    def create_item(item: ItemCreate) -> ItemBase:
        """Crea un nuevo item en Supabase"""
        db = get_supabase_client()
        try:
            response = db.table("items").insert(item.model_dump()).execute()
            if response.data:
                return response.data[0]
            raise HTTPException(status_code=400, detail="Failed to create item")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def get_items(limit: int, offset: int) -> list[ItemBase]:
        """Obtiene lista de items desde Supabase"""
        db = get_supabase_client()
        try:
            response = db.table("items").select("id, name, description, price, tax").range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def get_item_by_id(item_id: uuid.UUID) -> ItemBase:
        """Obtiene un item específico por ID"""
        db = get_supabase_client()
        try:
            response = db.table("items").select("*").eq("id", str(item_id)).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            raise HTTPException(status_code=404, detail="Item not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def update_item(item_id: uuid.UUID, item: ItemCreate) -> Item:
        """Actualiza un item existente"""
        db = get_supabase_client()
        try:
            response = db.table("items").update(item.model_dump()).eq("id", str(item_id)).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            raise HTTPException(status_code=404, detail="Item not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def delete_item(item_id: uuid.UUID) -> dict:
        """Elimina un item"""
        db = get_supabase_client()
        try:
            db.table("items").delete().eq("id", str(item_id)).execute()
            return {"message": "Item deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
