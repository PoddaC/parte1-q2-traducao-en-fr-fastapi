from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import translation
from app.services.translation_service import get_translator


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_translator()  # startup: carrega o modelo uma única vez
    yield


app = FastAPI(
    title="API de Tradução EN→FR (Helsinki-NLP/opus-mt-en-fr)",
    description="Recebe texto em inglês e devolve a tradução em francês.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(translation.router)
