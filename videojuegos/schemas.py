from pydantic import BaseModel, Field
from typing import Optional

class Videojuego(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    plataforma: str = Field(..., min_length=2, max_length=50)
    genero: str = Field(..., min_length=2, max_length=50)
    precio: float = Field(..., gt=0)
    
class VideojuegoInDB(Videojuego):
    id: str