from fastapi import FastAPI
from routers import videojuegos, usuarios


app = FastAPI()


#aca incluyo mi ruta de videojuegos
app.include_router(videojuegos.router)
app.include_router(usuarios.router)