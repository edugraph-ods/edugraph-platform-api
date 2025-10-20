from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database -mysql
    username: str = "root"
    password: str = "equinox1092"
    host: str = "localhost"
    port: int = 3306
    database: str = "edugraph"
    database_url: str = f"mysql+asyncmy://{username}:{password}@{host}:{port}/{database}"
    
    class Config:
        env_file = ".env"

settings = Settings()