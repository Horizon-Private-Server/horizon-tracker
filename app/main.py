import sys

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import column

from sqlalchemy.orm import Session, Query, DeclarativeBase
from starlette.responses import JSONResponse

from app.database import SessionLocal, Base
from app.models.dl import DeadlockedPlayer, DeadlockedOverallStats
from app.schemas.schemas import Pagination, LeaderboardEntry
from app.utils.query_helpers import get_stat_domains, get_available_stats_for_domain

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


@app.get("/api/dl/leaderboard/{domain}/{stat}")
def deadlocked_leaderboard(domain: str, stat: str, page: int = 1, session: Session = Depends(get_db)):

    stat_domains: dict[str, type[DeclarativeBase]] = get_stat_domains()

    if domain not in stat_domains:
        return JSONResponse(status_code=400, content={"error": f"Invalid stat domain '{domain}'."})

    stat_domain: type[DeclarativeBase] = stat_domains[domain]

    available_stats: list[str] = get_available_stats_for_domain(stat_domain)

    if stat not in available_stats:
        return JSONResponse(status_code=400, content={"error": f"Invalid stat field '{stat}'."})

    if page < 1:
        page = 1
    else:
        page -= 1

    query: Query = session.query(DeadlockedPlayer) \
        .join(stat_domain) \
        .add_columns(column(stat)) \
        .order_by(getattr(stat_domain, stat).desc(), DeadlockedPlayer.horizon_id.asc())

    results: list[tuple[DeadlockedPlayer, int]] = list(query.offset(100 * page).limit(100))

    count = query.count()

    return JSONResponse(
        status_code=200,
        content={
            "count": count,
            "results": [
                {
                    "horizon_id": result.horizon_id,
                    "username": result.username,
                    "score": score,
                    "rank": (100 * page) + index + 1
                }
                for index, (result, score)
                in enumerate(results)
            ]
        }
    )
