from pydantic import BaseModel, Field
from typing import Optional


#este model0 para crear un videojuego
class VideoJuegoCrear(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    plataforma: str = Field(..., min_length=2, max_length=50)
    genero: str = Field(..., min_length=2, max_length=50)
    precio: float = Field(..., gt=0)

#Este model es para actualizar un videojuego cuyos campos sean opcionales
class VideoJuegoActualizar(BaseModel):
    nombre: Optional[str] = None
    plataforma: Optional[str] = None
    genero: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)



#Este sera el modelo de respuesta que se enviara al cliente incluye id
class VideoJuegoInDB(VideoJuegoCrear):
    id: str