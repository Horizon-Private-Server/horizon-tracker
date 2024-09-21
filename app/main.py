from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal

from app.routers.dl.stats import router as deadlocked_stats_router
from app.routers.uya.stats import router as uya_stats_router

ALLOWED_ORIGINS: list[str] = [
    "https://www.rac-horizon.com",
    "https://rac-horizon.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add sub-APIs.
app.include_router(deadlocked_stats_router)
app.include_router(uya_stats_router)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """
    The following view is designed for sanity checks to ensure that the API is functional.
    """
    return {"message": "Hello World"}

