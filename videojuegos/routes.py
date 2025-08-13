from fastapi import APIRouter, HTTPException
from bson import ObjectId
from config.database import db
from .schemas import Videojuego, VideojuegoInDB

router = APIRouter(prefix="/videojuegos", tags=["videojuegos"])

def videojuego_helper(vj) -> dict:
    return{
        "id": str(vj["_id"]),
        "nombre": vj["nombre"],
        "plataforma": vj["plataforma"],
        "genero": vj["genero"],
        "precio": vj["precio"]
    }


@router.post("/", response_model=VideojuegoInDB)
async def crear_videojuego(videojuego: Videojuego):
    nuevo = await db.videojuegos.insert_one(videojuego.model_dump())
    creado = await db.videojuegos.find_one({"_id": nuevo.inserted_id})
    return videojuego_helper(creado)


@router.get("/", response_model=list[VideojuegoInDB])
async def listar_videojuegos():
    videojuegos = []
    async for vj in db.videojuegos.find():
        videojuegos.append(videojuego_helper(vj))
    return videojuegos


@router.get("/{id}", response_model=VideojuegoInDB)
async def obtener_videojuegos(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    
    vj = await db.videojuegos.find_one({"_id": ObjectId(id)})
    if not vj:
        raise HTTPException(status_code=404, detail="videojuego no encontrado")
    return videojuego_helper(vj)


@router.put("/{id}", response_model=VideojuegoInDB)
async def actualizar_videojuego(id: str, videojuego: Videojuego):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    
    actualizado = await db.videojuegos.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": videojuego.model_dump()},
        return_document=True
    )
    
    if not actualizado:
        raise HTTPException(status_code=404, detail="videojuego no actualizado")
    return videojuego_helper(actualizado)


@router.delete("/{id}")
async def eliminar_videojuego(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    
    eliminado = await db.videojuegos.find_one_and_delete({"_id": ObjectId(id)})
    if not eliminado:
        raise HTTPException(status_code=404, detail="videojuego no eliminado")
    return {"message": "videojuego eliminado exitosamente"}

