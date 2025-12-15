from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Test Application",
    description="Test application for CI/CD pipeline",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "Application is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
