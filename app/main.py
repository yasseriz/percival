from fastapi import FastAPI
from app.routes.api import router as api_router

app = FastAPI()
app.include_router(api_router)

# Optional: Startup and Shutdown events
@app.on_event("startup")
async def startup_event():
    # Initialize resources
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup resources
    pass