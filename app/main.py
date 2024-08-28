from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import column

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.dl import DeadlockedPlayer, DeadlockedOverallStats
from horizon.parsing.deadlocked_stats import convert_rank_to_skill_level

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/rank")
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):

    results = session.query(DeadlockedPlayer) \
        .join(DeadlockedOverallStats) \
        .add_columns(column("rank")) \
        .order_by(
            DeadlockedOverallStats.rank.desc(), DeadlockedPlayer.horizon_id.asc()
        ).limit(100)

    return [
        {
            "username": player.username,
            "horizon_id": player.horizon_id,
            "rank": rank,
            "skill_level": convert_rank_to_skill_level(rank)
        }
        for player, rank
        in results
    ]
