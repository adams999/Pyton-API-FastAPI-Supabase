from fastapi import FastAPI, HTTPException
from db import DbDependency
from models import Item, ItemBase, ItemCreate
from config import settings
import uuid

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

@app.get("/")
async def root():
    return {"message": "Hello World - Connected to Supabase"}


@app.post("/items", response_model=ItemBase)
async def create_item(item: ItemCreate, db: DbDependency):
    """Crea un nuevo item en Supabase"""
    try:
        response = db.table("items").insert(item.model_dump()).execute()
        if response.data:
            return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/items", response_model=list[ItemBase])
async def get_items(limit: int = 10, offset: int = 0, db: DbDependency = None):
    """Obtiene lista de items desde Supabase"""
    try:
        response = db.table("items").select("id, name, description, price, tax").range(offset, offset + limit - 1).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/items/{item_id}", response_model=ItemBase)
async def get_item(item_id: uuid.UUID, db: DbDependency):
    """Obtiene un item específico por ID"""
    try:
        response = db.table("items").select("*").eq("id", str(item_id)).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: uuid.UUID, item: ItemCreate, db: DbDependency):
    """Actualiza un item existente"""
    try:
        response = db.table("items").update(item.model_dump()).eq("id", str(item_id)).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/items/{item_id}")
async def delete_item(item_id: uuid.UUID, db: DbDependency):
    """Elimina un item"""
    try:
        db.table("items").delete().eq("id", str(item_id)).execute()
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))