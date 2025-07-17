from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database: str
    database_host: str
    database_port: int
    database_user: str
    database_passwd: str
    
    static_app_dir: str

    notify_admin_url: str

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
