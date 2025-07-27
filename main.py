from fastapi import FastAPI
from app.routes import user_routes
from app.routes import scan_routes
from app.routes import header_routes


# Initialize the FastAPI application
app = FastAPI(
    title="Security Header Analyzer API",
    description="API for analyzing and managing security headers.",
    version="1.0.0",
)

# Register route modules
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(scan_routes.router, prefix="/scans", tags=["Scans"])
app.include_router(header_routes.router, prefix="/headers", tags=["Headers"])


@app.get("/")
def read_root():
    """Root health check endpoint."""
    return {"message": "Security Headers Analyzer is live"}


# This ensures the app runs if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

