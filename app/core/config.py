from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Глобальные настройки приложения.

    Переменные окружения:
        * SET_DEBUG
        * SET_SECRET_KEY
        * SET_JWT_LIFETIME
        * SET_APP_NAME
        * SET_APP_DESC
        * SET_VERSION
        * SET_DOCS_URL
        * SET_DATABASE_URL

    Атрибуты:
        DEBUG (bool): Обязательно отключить в проде.
        SECRET_KEY (str): Секретное слово.
        JWT_LIFETIME (int): Продолжительность работы JWT-токена.
        APP_NAME (str): Название FastAPI проекта.
        APP_DESC (str): Описание FastAPI проекта.
        VERSION (str): Версия проекта.
        DOCS_URL (str): Адрес Swagger UI.
        DATABASE_URL (str): Конфигурация базы данных.
    """

    DEBUG: bool = True
    SECRET_KEY: str = "random text"
    JWT_LIFETIME: int = 3600
    APP_NAME: str = "App Name"
    APP_DESC: str = "App description."
    VERSION: str = "0.1.0"
    DOCS_URL: str = "/"
    DATABASE_URL: str = "sqlite+aiosqlite:///./fastapi.db"

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_prefix = "SET_"


settings = Settings()
