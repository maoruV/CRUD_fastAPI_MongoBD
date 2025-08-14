from passlib.context import CryptContext

# configuuramos el bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Generamos un hash seguro para la contraseña"""
    return pwd_context.hash(password)


def verificar_password(text_password: str, hashed_password: str) -> bool:
    """verificamos que la contraseña  de texto plano concuerde con el hash"""
    return pwd_context.verify(text_password, hashed_password)