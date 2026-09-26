import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.views import router as api_router
from core.settings import Base, engine, ensure_database_schema

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
uploads_dir = os.path.join(BASE_DIR, "uploads")
os.makedirs(os.path.join(uploads_dir, "categories"), exist_ok=True)
os.makedirs(os.path.join(uploads_dir, "products"), exist_ok=True)
os.makedirs(os.path.join(uploads_dir, "payments"), exist_ok=True)
os.makedirs(os.path.join(uploads_dir, "complaints"), exist_ok=True)

# Initialize database tables
ensure_database_schema()

app = FastAPI(
    title="Power Solution API",
    version="1.0.0",
)

# CORS middleware for Flutter integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include API Router
app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Power Solution API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
