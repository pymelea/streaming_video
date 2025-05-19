import models.category
import models.subtitle
import models.video

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.database import engine
from api.api import api_router

# Create tables in the database - order matters for foreign key relationships
# Create Category tables first (referenced by Video)
models.category.Base.metadata.create_all(bind=engine)
# Create Video tables next
models.video.Base.metadata.create_all(bind=engine)
# Create Subtitle tables last (depends on Video)
models.subtitle.Base.metadata.create_all(bind=engine)
# Create tables for other models if needed

# Create application in FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for streaming videos",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Health check endpoint to verify that the API is working
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
