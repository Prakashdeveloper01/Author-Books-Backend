from app.api import api_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from app.config import CONFIG_SETTINGS


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=CONFIG_SETTINGS.PROJECT_NAME,
    version=CONFIG_SETTINGS.API_VERSION,
    description=CONFIG_SETTINGS.DESCRIPTION,
    docs_url="/docs" if CONFIG_SETTINGS.IS_SWAGGER_ENABLED else None,
    redoc_url="/redoc" if CONFIG_SETTINGS.IS_SWAGGER_ENABLED else None,
    openapi_url="/openapi.json" if CONFIG_SETTINGS.IS_SWAGGER_ENABLED else None,
    lifespan=lifespan,
    debug=CONFIG_SETTINGS.FASTAPI_DEBUG,
    root_path=CONFIG_SETTINGS.ROOT_PATH,
)


@app.get("/", tags=["Health"])
async def root():
    """Root health check endpoint."""
    return {"status": "ok", "message": "Backend is running"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Backend health check endpoint."""
    return {"status": "ok", "message": "Backend is ready"}


app.include_router(api_router)

# Mount files directory
if not os.path.exists("files"):
    os.makedirs("files")
app.mount("/files", StaticFiles(directory=os.path.abspath("files")), name="files")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["Authorization", "Content-Disposition"],
)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 7999))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
