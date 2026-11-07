"""
FastAPI Production Application Entrypoint.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.dependencies import get_predictor
from app.routes.catalog import router as catalog_router
from app.routes.health import router as health_router
from app.routes.predict import router as predict_router
from src.utils.logger import get_logger

logger = get_logger("app_main")

# Setup directories
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_IMAGES_DIR = Path("data/sample_images")
SAMPLE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager: loads model and resources at startup.
    """
    logger.info("Initializing PhytoAI Plant Disease Detection service...")
    predictor = get_predictor()
    app.state.predictor = predictor
    logger.info(f"Predictor initialized with engine: {predictor.model_type}")

    yield

    logger.info("Shutting down Plant Disease Detection service...")


app = FastAPI(
    title="PhytoAI - Plant Disease Detection & Advisory API",
    description="Production-grade AI vision API and agronomic diagnostic service for 38 plant foliage diseases across 14 crops.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Assets & Templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
if SAMPLE_IMAGES_DIR.exists():
    app.mount("/data/sample_images", StaticFiles(directory=str(SAMPLE_IMAGES_DIR)), name="sample_images")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Register Routers
app.include_router(health_router)
app.include_router(predict_router)
app.include_router(catalog_router)


@app.get("/", response_class=HTMLResponse, tags=["Web Interface"])
async def render_dashboard(request: Request):
    """
    Renders the responsive agronomic diagnostic dashboard.
    """
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
