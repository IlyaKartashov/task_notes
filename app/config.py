from pydantic_settings import BaseSettings
# так же отсюда из Settings могут браться переменные окружения, будет доступ через <settings.> !

class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./notes_app_db.sqlite3"
    db_echo: bool = True

settings = Settings()
