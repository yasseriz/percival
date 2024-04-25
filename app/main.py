from fastapi import FastAPI
import uvicorn
from app.routes.api import router as api_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
