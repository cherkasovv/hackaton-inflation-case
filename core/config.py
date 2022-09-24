from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str
    database_url: str

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()