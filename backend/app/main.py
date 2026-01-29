"""GreenPulse Backend - FastAPI Main Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.routes import climate_router
from app.routes.ai import router as ai_router
from app.routes.cron import router as cron_router
from app.routes.land_data import router as land_data_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("=" * 50)
    print("GreenPulse API Starting...")
    print(f"Environment: {'Production' if os.getenv('DEBUG', 'False') == 'False' else 'Development'}")
    print(f"Port: {os.getenv('PORT', 8000)}")
    print("=" * 50)
    yield
    # Shutdown
    print("GreenPulse API Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title=os.getenv("APP_NAME", "GreenPulse API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="AI-powered climate risk and resilience platform API for Africa",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://greenpulse.vercel.app").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "online",
        "message": "GreenPulse API - Guarding the Land. Empowering the People.",
        "version": os.getenv("APP_VERSION", "1.0.0"),
    "timestamp": datetime.now(timezone.utc).isoformat(),
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
    "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "api": "running",
            "database": "connected",
            "telegram_bot": "active",
            "whatsapp": "disabled"
        },
        "features": {
            "ai_chat": os.getenv("ENABLE_AI_CHAT", "True") == "True",
            "alerts": True,
            "climate_detection": True
        },
        "version": os.getenv("APP_VERSION", "1.0.0")
    }

# Include routers
app.include_router(climate_router)
app.include_router(ai_router)
app.include_router(cron_router)
app.include_router(land_data_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True") == "True"
    )
