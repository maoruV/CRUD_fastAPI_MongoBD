from pydantic import BaseModel, Field, EmailStr

class Usuario(BaseModel):
    nombre_usario: str = Field(...,min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    
class UsuarioInDB(Usuario):
    id: str