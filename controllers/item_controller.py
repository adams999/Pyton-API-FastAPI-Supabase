from db import DbDependency
from models import Item, ItemBase, ItemCreate
from services import ItemService
import uuid


class ItemController:
    """Controlador que maneja las peticiones HTTP para items"""

    @staticmethod
    async def create_item(item: ItemCreate, db: DbDependency) -> ItemBase:
        """Endpoint para crear un nuevo item"""
        return ItemService.create_item(item, db)

    @staticmethod
    async def get_items(limit: int = 10, offset: int = 0, db: DbDependency = None) -> list[ItemBase]:
        """Endpoint para obtener lista de items"""
        return ItemService.get_items(limit, offset, db)

    @staticmethod
    async def get_item(item_id: uuid.UUID, db: DbDependency) -> ItemBase:
        """Endpoint para obtener un item específico"""
        return ItemService.get_item_by_id(item_id, db)

    @staticmethod
    async def update_item(item_id: uuid.UUID, item: ItemCreate, db: DbDependency) -> Item:
        """Endpoint para actualizar un item"""
        return ItemService.update_item(item_id, item, db)

    @staticmethod
    async def delete_item(item_id: uuid.UUID, db: DbDependency) -> dict:
        """Endpoint para eliminar un item"""
        return ItemService.delete_item(item_id, db)
