from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_ID: int
    API_HASH: str
    BOT_TOKEN: str
    DB_URL: str
    DB_CREATE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
