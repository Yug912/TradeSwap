import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import match, health


def _cors_origins() -> list[str]:
    configured_origins = os.getenv(
        "FASTAPI_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    return [origin.strip() for origin in configured_origins.split(",") if origin.strip()]


app = FastAPI(title="TradeSwap Matching API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(match.router)