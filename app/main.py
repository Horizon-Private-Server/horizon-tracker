from fastapi import Depends, FastAPI

from app.database import SessionLocal

from app.routers.dl.stats import router as deadlocked_stats_router

app = FastAPI()

# Add sub-APIs.
app.include_router(deadlocked_stats_router)


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

