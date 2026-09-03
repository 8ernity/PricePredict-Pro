import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.db.database import Base, engine
from app.core.config import PROJECT_ROOT

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PricePredict Pro API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)

# Serve Frontend Static Files
frontend_path = os.path.join(PROJECT_ROOT, "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
