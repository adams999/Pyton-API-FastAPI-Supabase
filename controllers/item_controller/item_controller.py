from models import Item, ItemBase, ItemCreate
from services import ItemService
import uuid


class ItemController:
    """Controlador que maneja las peticiones HTTP para items"""

    @staticmethod
    async def create_item(item: ItemCreate) -> ItemBase:
        """Endpoint para crear un nuevo item"""
        return ItemService.create_item(item)

    @staticmethod
    async def get_items(limit: int = 10, offset: int = 0) -> list[ItemBase]:
        """Endpoint para obtener lista de items"""
        return ItemService.get_items(limit, offset)

    @staticmethod
    async def get_item(item_id: uuid.UUID) -> ItemBase:
        """Endpoint para obtener un item específico"""
        return ItemService.get_item_by_id(item_id)

    @staticmethod
    async def update_item(item_id: uuid.UUID, item: ItemCreate) -> Item:
        """Endpoint para actualizar un item"""
        return ItemService.update_item(item_id, item)

    @staticmethod
    async def delete_item(item_id: uuid.UUID) -> dict:
        """Endpoint para eliminar un item"""
        return ItemService.delete_item(item_id)
