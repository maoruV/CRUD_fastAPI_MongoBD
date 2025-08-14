from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from typing import Optional


#Configuracion con Pydantic 2
class Settings(BaseSettings):
    MONGODB_URI: str
    DB_NAME: str = "tienda"
    
    class Config:
        env_file =".env"  # Leemos variables desde .env
        

settings = Settings()



client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]