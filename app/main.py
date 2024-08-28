from fastapi import Depends, FastAPI, HTTPException

from app.database import SessionLocal

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
