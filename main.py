from fastapi import FastAPI
from config import settings
from routes import item_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Incluir routers
app.include_router(item_router)

@app.get("/")
async def root():
    return {"message": "Hello World - Connected to Supabase"}