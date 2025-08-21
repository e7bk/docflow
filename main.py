from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from shared.database import init_database
from documents.routes import router as documents_router

# Modern FastAPI lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_database()
    print("🚀 DocFlow API is ready!")
    print("📚 Your upload validation is active!")
    print("🔗 API docs at: http://localhost:8000/docs")
    yield
    # Shutdown (if needed)

# Create FastAPI app with modern lifespan
app = FastAPI(
    title="DocFlow - Document Processing System",
    description="Your document upload and processing system with bulletproof validation!",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include document routes
app.include_router(
    documents_router, 
    prefix="/documents", 
    tags=["Documents"]
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to DocFlow API! 🚀",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "File upload with validation",
            "Multiple document types supported", 
            "Security validation (MIME/extension matching)",
            "Size limits (10MB)",
            "User directory structure"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "validation": "active", 
        "upload_limit": "10MB",
        "supported_types": ["PDF", "Word", "Excel", "CSV"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
