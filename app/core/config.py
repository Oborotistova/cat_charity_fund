from pydantic import BaseSettings


MIN_PASS_LEN = 3
LIFETIME_SEC = 3600


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot.'
    description: str = 'Фонд собирает пожертвования на целевые проекты'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
