from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import importlib

from . import config  # noqa: F401
from .api.routes import crop, fertilizer, irrigation, price, weather
from .model_service import MODEL_ARTIFACTS, MODEL_DIR

yield_route = importlib.import_module(".api.routes.yield", package=__package__)

app = FastAPI(
    title="AgriSense AI API",
    description="Agricultural decision support powered by five machine-learning models and live weather data.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crop.router)
app.include_router(fertilizer.router)
app.include_router(irrigation.router)
app.include_router(price.router)
app.include_router(yield_route.router)
app.include_router(weather.router)


@app.get("/health")
def health() -> dict[str, str | int]:
    available = sum((MODEL_DIR / artifact).is_file() for artifact in MODEL_ARTIFACTS.values())
    return {
        "status": "ok" if available == len(MODEL_ARTIFACTS) else "degraded",
        "service": "AgriSense AI API",
        "models_available": available,
        "models_total": len(MODEL_ARTIFACTS),
    }
