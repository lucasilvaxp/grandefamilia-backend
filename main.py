"""
FastAPI Backend - Fashion Catalog API
Entry point for the backend server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import products, categories, settings, upload
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Fashion Catalog API",
    description="Backend API for Fashion E-commerce Catalog - Loja A Grande Família",
    version="1.0.0"
)

# CORS Configuration - Robust handling for string or list
# In production, replace with your Vercel frontend URL
cors_value = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://yourdomain.vercel.app")

# Handle both string (comma-separated) and list formats
if isinstance(cors_value, str):
    origins = [origin.strip() for origin in cors_value.split(",")]
elif isinstance(cors_value, list):
    origins = cors_value
else:
    # Fallback to localhost if type is unexpected
    origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(settings.router)
app.include_router(upload.router)

@app.get("/")
async def root():
    return {
        "message": "Fashion Catalog API - Loja A Grande Família",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    return {"status": "healthy", "service": "fastapi-backend"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
