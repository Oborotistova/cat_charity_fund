from pydantic import BaseSettings, EmailStr
from typing import Optional

class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot.'
    description: str = 'Фонд собирает пожертвования на различные целевые проекты'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    


    class Config:
        env_file = '.env'


settings = Settings() 