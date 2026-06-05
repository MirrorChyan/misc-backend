from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database: str
    database_host: str
    database_port: int
    database_user: str
    database_passwd: str
    
    static_app_dir: str

    notify_admin_url: str

    admin_secret: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()
