from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from database import db
from models.videojuegos import VideoJuegoCrear, VideoJuegoActualizar, VideoJuegoInDB

router = APIRouter(prefix="/videojuegos", tags=["videojuegos"])


#Esta funcion se utiliza para convertir MongoDB a un diccionario que Fastapi pueda manejar
def videojuego_convertidor(videojuego) -> dict:
    return{
        "id": str(videojuego["_id"]),
        "nombre": videojuego["nombre"],
        "plataforma": videojuego["plataforma"],
        "genero": videojuego["genero"],
        "precio": videojuego["precio"]
    }


#metodo post para crera un videojuego
@router.post("/", response_model=VideoJuegoInDB)
async def crear_videojuego(videojuego: VideoJuegoCrear):
    nuevo = videojuego.model_dump()
    resultado = await db.videojuegos.insert_one(nuevo)
    creado = await db.videojuegos.find_one({"_id": resultado.inserted_id})
    return videojuego_convertidor(creado)



#metodo get para listar los videojuegos que hay en las base de datos
# @router.get("/", response_model=list[VideoJuegoInDB])
# async def listar_videojuegos():
#     #find me trae todos los documentos de la coleccion y con to_list(100) limitamos a 100 esto evita que se carguen todos
#     #en memoria y se bloquee la aplicacion
#     videojuegos =  await db.videojuegos.find().to_list(100)
#     return [videojuego_convertidor(videojuego) for videojuego in videojuegos]


# ✅ Buscar videojuegos con filtros + rango de precios + ordenamiento + paginación
@router.get("/", response_model=dict)
async def listar_videojuegos(
    nombre: str | None = Query(None, description="Buscar por nombre"),
    plataforma: str | None = Query(None, description="Buscar por plataforma"),
    genero: str | None = Query(None, description="Buscar por género"),
    precio: float | None = Query(None, description="Buscar por precio exacto"),
    min_precio: float | None = Query(None, description="Precio mínimo"),
    max_precio: float | None = Query(None, description="Precio máximo"),
    ordenar_por: str | None = Query(None, description="Campo para ordenar: nombre, plataforma, precio, genero"),
    direccion: str | None = Query("asc", description="asc o desc"),
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad de resultados por página (máx 100)")
):
    filtros = {}

    if nombre:
        filtros["nombre"] = {"$regex": nombre, "$options": "i"}

    if plataforma:
        filtros["plataforma"] = {"$regex": plataforma, "$options": "i"}

    if genero:
        filtros["genero"] = {"$regex": genero, "$options": "i"}

    if precio:
        filtros["precio"] = precio

    if min_precio is not None or max_precio is not None:
        rango = {}
        if min_precio is not None:
            #$gte para realizar consultas que filtran el valor de un campo es >=
            rango["$gte"] = min_precio
        if max_precio is not None:
            #$lte para realizar consultas que filtran el valor de un campo es <=
            rango["$lte"] = max_precio
        filtros["precio"] = rango

    #  Preparo la consulta
    vj_consulta = db.videojuegos.find(filtros)

    #  Aplicar ordenamiento si corresponde
    if ordenar_por:
        direccion_num = 1 if direccion == "asc" else -1
        vj_consulta = vj_consulta.sort(ordenar_por, direccion_num)

    #  Paginación
    total = await db.videojuegos.count_documents(filtros)
    skip = (page - 1) * limit
    vj_consulta = vj_consulta.skip(skip).limit(limit)

    videojuegos = await vj_consulta.to_list(length=limit)

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total // limit) + (1 if total % limit else 0),
        "items": [
            {
                "id": str(v["_id"]),
                "nombre": v["nombre"],
                "plataforma": v["plataforma"],
                "precio": v["precio"],
                "genero": v["genero"],
            }
            for v in videojuegos
        ]
    }


#metodo get para listar los videojuegos por id que hay en las base de datos
@router.get("/{id}", response_model=VideoJuegoInDB)
async def obtener_videojuego(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    
    videojuego = await db.videojuegos.find_one({"_id": ObjectId(id)})
    if not videojuego:
        raise HTTPException(status_code=404, detail="videojuego no encontrado")
    return videojuego_convertidor(videojuego)


#metod put para que podamos actualizar un videojuego en la base de datos
@router.put("/{id}", response_model=VideoJuegoInDB)
async def actualizar_videojuego(id: str, videojuego: VideoJuegoActualizar):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    
    #Conviertimos el objeto en un diccionario con pares clave-valor, y con la condicion se filtra para que 
    #solo entren en el diccionario los campos que no son None
    actualizacion = {k: v for k, v in videojuego.model_dump().items() if v is not None}
    
    if not actualizacion:
        raise HTTPException(status_code=400, detail="No se enviaron los campos para actualizar")
    
    #"$set" se usa para modificar  o agregar campos al documento, si existe reeplaza su valor
    #si existe lo crea con el valor especificado
    actualizado = await db.videojuegos.update_one({"_id": ObjectId(id)}, {"$set": actualizacion})
    
    if actualizado.matched_count == 0:
        raise HTTPException(status_code=404, detail="El videojuego no se encontro")
    
    actualizado = await db.videojuegos.find_one({"_id": ObjectId(id)})
    return videojuego_convertidor(actualizado)


#metodo para eliminar un videio juego en la base de datos
@router.delete("/{id}")
async def eliminar_videojuego(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    
    eliminado = await db.videojuegos.delete_one({"_id": ObjectId(id)})
    if eliminado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="videojuego no encontrado")
    return {"message": "videojuego eliminado exitosamente"}

