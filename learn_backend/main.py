from fastapi import FastAPI

app = FastAPI(
    title="Learn Backend API",
    description="A step-by-step learning API for backend concepts",
    version="0.1.0",
)


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok", "message": "Service is running"}
