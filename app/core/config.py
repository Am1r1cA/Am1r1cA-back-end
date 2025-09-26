from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "AmiricA APIs"
    SECRET_KEY: str = "changeme_replace_with_secure_random_hex_64"
    JWT_SECRET: str = "changeme_replace_with_secure_random_hex_64"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/postgres"
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1,0.0.0.0"
    
    class Config:
        env_file = ".env"
        extra = "ignore" 

settings = Settings()
