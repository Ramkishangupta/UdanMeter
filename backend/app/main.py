import logging
from logging.handlers import RotatingFileHandler
import time
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal, IS_SQLITE
from app.api.routes import router
from app.data_pipeline.repository import data_repository

# 1. Configure Rotating File Logger using environment settings
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "apix_server.log")

log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

rotating_file_handler = RotatingFileHandler(
    LOG_FILE_PATH,
    maxBytes=settings.LOG_MAX_BYTES,
    backupCount=settings.LOG_BACKUP_COUNT,
    encoding="utf-8"
)
rotating_file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

logging.basicConfig(
    level=log_level,
    handlers=[rotating_file_handler, stream_handler]
)

logger = logging.getLogger("apix_main")
db_type = "SQLite (Local fallback)" if IS_SQLITE else "PostgreSQL (Production Pool)"
logger.info(f"Initializing MoSPI APIx Engine ({settings.ENVIRONMENT})...")
logger.info(f"Database Engine: {db_type}")
logger.info(f"Server log path: {LOG_FILE_PATH} (Rotating: {settings.LOG_MAX_BYTES // (1024*1024)}MB x {settings.LOG_BACKUP_COUNT} backups)")

# 2. Create Database Tables
Base.metadata.create_all(bind=engine)

# 3. Seed Route Weights
db = SessionLocal()
try:
    data_repository.initialize_route_weights(db)
    logger.info("DGCA Primary Route Traffic Weights initialized successfully.")
except Exception as e:
    logger.error(f"Error seeding route weights: {e}")
finally:
    db.close()

# 4. Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MoSPI & RBI Real-time Airfare Price Index (APIx) Automated Web Scraping & Index Engine (SIH 26056)"
)

# 5. Enable CORS for Frontend UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Detailed Request & Response Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}ms"
    
    logger.info(
        f"HTTP {request.method} {request.url.path} | Status: {response.status_code} | "
        f"IP: {client_ip} | Duration: {formatted_process_time}"
    )
    
    response.headers["X-Process-Time"] = formatted_process_time
    return response

app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint health check accessed.")
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_type,
        "organization": "National Statistical Office (NSO), MoSPI",
        "log_file": LOG_FILE_PATH,
        "log_rotation": f"RotatingFileHandler ({settings.LOG_MAX_BYTES // (1024*1024)}MB x {settings.LOG_BACKUP_COUNT} backups max)",
        "docs_url": "/docs",
        "api_v1_summary": "/api/v1/apix/summary"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=(settings.ENVIRONMENT == "development"))
