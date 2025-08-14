from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    email: EmailStr #con esto validamos que sea un email valido

class UsuarioCrear(UsuarioBase):
    password: str = Field(..., min_length=6)

class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)

class UsuarioDB(UsuarioBase):
    id: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str