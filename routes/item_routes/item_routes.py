from fastapi import APIRouter
from controllers import ItemController
from models import Item, ItemBase, ItemCreate
from db import DbDependency
import uuid

router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.post("", response_model=ItemBase)
async def create_item(item: ItemCreate, db: DbDependency):
    """Crea un nuevo item en Supabase"""
    return await ItemController.create_item(item, db)


@router.get("", response_model=list[ItemBase])
async def get_items(limit: int = 10, offset: int = 0, db: DbDependency = None):
    """Obtiene lista de items desde Supabase"""
    return await ItemController.get_items(limit, offset, db)


@router.get("/{item_id}", response_model=ItemBase)
async def get_item(item_id: uuid.UUID, db: DbDependency):
    """Obtiene un item específico por ID"""
    return await ItemController.get_item(item_id, db)


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: uuid.UUID, item: ItemCreate, db: DbDependency):
    """Actualiza un item existente"""
    return await ItemController.update_item(item_id, item, db)


@router.delete("/{item_id}")
async def delete_item(item_id: uuid.UUID, db: DbDependency):
    """Elimina un item"""
    return await ItemController.delete_item(item_id, db)
