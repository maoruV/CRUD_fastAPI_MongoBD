from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    mongo_db: str

    class Config:
        env_file = ".env"  # Archivo donde buscar las variables
        env_file_encoding = "utf-8"

# Instancia global de configuración
settings = Settings()
