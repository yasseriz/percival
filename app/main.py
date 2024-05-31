from fastapi import FastAPI
import uvicorn
from app.routes.api import router as api_router
import logging
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("uvicorn")


app = FastAPI()
app.include_router(api_router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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
