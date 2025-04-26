from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database: str
    database_host: str
    database_port: int
    database_user: str
    database_passwd: str
    icp_beian: str
    icp_url: str
    icp_entity: str

    class Config:
        env_file = ".env"


settings = Settings()
