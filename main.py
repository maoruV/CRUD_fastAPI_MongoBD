from fastapi import FastAPI
from routers import videojuegos


app = FastAPI(title="API Tienda", version="1.0.0")


#aca incluyo mi ruta de videojuegos
app.include_router(videojuegos.router)
