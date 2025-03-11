from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database: str
    database_host: str
    database_port: int
    database_user: str
    database_passwd: str

    class Config:
        env_file = ".env"


settings = Settings()
