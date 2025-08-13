from fastapi import FastAPI
from config.database import db
from videojuegos.routes import router as videojuegos_router


app = FastAPI(title="API Tienda", version="1.0.0")


app.include_router(videojuegos_router)
