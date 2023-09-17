from fastapi import FastAPI

from app.core.config import settings
from app.core.router import main_router

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESC,
    debug=settings.DEBUG,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
)
app.include_router(main_router)
