from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import db
from models.usuarios import UsuarioCrear, UsuarioActualizar, UsuarioDB, UsuarioLogin
from core.security import hash_password, verificar_password

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=dict)
async def crear_usuario(usuario: UsuarioCrear):
    #Verificamos si existe el email
    existe = await db.usuarios.find_one({"email": usuario.email})
    if existe:
        raise HTTPException(status_code=400, detail="El email ya existe")
    
    #aca en este momento haseamos la contraseña
    usuario_dict = usuario.model_dump()
    usuario_dict["password"] = hash_password(usuario.password)
    
    resultado = await db.usuarios.insert_one(usuario_dict)
    return {"id": str(resultado.inserted_id), "nombre": usuario.nombre, "email": usuario.email}


@router.get("/", response_model=list[UsuarioDB])
async def listar_usuarios():
    usuarios = await db.usuarios.find().to_list(100)
    return [
        {"id": str(u["_id"]), "nombre": u["nombre"], "email": u["email"]}
        for u in usuarios
    ]


@router.get("/{id}", response_model=UsuarioDB)
async def obtener_usuario(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="id no valido")
    
    usuario = await db.usuarios.find_one({"_id": ObjectId(id)})
    if not usuario:
        raise HTTPException(status_code=404, detail="No se encontro el usuario")
    
    return {"id": str(usuario["_id"]), "nombre": usuario["nombre"], "email": usuario["email"]}


@router.put("/{id}", response_model=dict)
async def actualizar_usuario(id: str, usuario: UsuarioActualizar):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="id no valido")
    
    actualizacion = {k: v for k, v in usuario.model_dump().items() if v is not None}
    
    #aqui actualizamos la contraseña para hashearla
    if "password" in actualizacion:
        actualizacion["password"] = hash_password(actualizacion["password"])
    
    resultado = await db.usuarios.update_one(
        {"_id": ObjectId(id)}, {"$set": actualizacion}
    )
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="No se encontro el usuario")
    
    return {"mensaje": "Se actualizo el usuario correctamente"}


@router.delete("/{id}", response_model=dict)
async def eliminar_usuario(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="id no valido")
    
    resultado = await db.usuarios.delete_one({"_id": ObjectId(id)})
    
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No se encontro el usuario")
    
    return {"mensaje": "Se elimino el usuario correctamente"}


# Creo el login basico  de los usuarios
@router.post("/login")
async def login(datos: UsuarioLogin):
    usuario = await db.usuarios.find_one({"email": datos.email})
    if not usuario:
        raise HTTPException(status_code=400, detail="No se encontro el usuario")
    
    if not verificar_password(datos.password, usuario["password"]):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    return {"mensaje": "login existoso"}