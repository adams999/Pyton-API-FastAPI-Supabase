from fastapi import APIRouter
from controllers import ItemController
from models import Item, ItemBase, ItemCreate
import uuid

router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.post("", response_model=ItemBase)
async def create_item(item: ItemCreate):
    """Crea un nuevo item en Supabase"""
    return await ItemController.create_item(item)


@router.get("", response_model=list[ItemBase])
async def get_items(limit: int = 10, offset: int = 0):
    """Obtiene lista de items desde Supabase"""
    return await ItemController.get_items(limit, offset)


@router.get("/{item_id}", response_model=ItemBase)
async def get_item(item_id: uuid.UUID):
    """Obtiene un item específico por ID"""
    return await ItemController.get_item(item_id)


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: uuid.UUID, item: ItemCreate):
    """Actualiza un item existente"""
    return await ItemController.update_item(item_id, item)


@router.delete("/{item_id}")
async def delete_item(item_id: uuid.UUID):
    """Elimina un item"""
    return await ItemController.delete_item(item_id)
