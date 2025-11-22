from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT
    secret_key: str = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database -mysql
    username: str = "edugraph"
    password: str = "Acceso09"
    host: str = "edugraph.mysql.database.azure.com"
    port: int = 3306
    database: str = "edugraph"
    database_url: str = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
    
    # Password reset
    password_reset_token_expire_minutes: int = 60
    password_reset_url_template: str = "https://edugraph-front-end.vercel.app/auth/reset-password?token={token}&uid={uid}"

    # Email (SMTP)
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_username: str = "edugraphplatform@gmail.com"
    smtp_password: str = "zpujothfkelldojz"
    smtp_sender: str | None = None

    # CORS ORIGINS
    backend_cors_origins: List[str] = ["http://localhost:3000", "http://192.168.18.213:3000", "https://edugraph-front-end.vercel.app"]
    
    class Config:
        env_file = ".env"

settings = Settings()