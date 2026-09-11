import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.views import router as api_router
from core.settings import Base, engine, ensure_database_schema

os.makedirs("uploads/categories", exist_ok=True)
os.makedirs("uploads/products", exist_ok=True)

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

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API Router
app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Power Solution API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
