from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import column

from sqlalchemy.orm import Session, Query, DeclarativeBase

from app.database import SessionLocal
from app.models.dl import DeadlockedPlayer
from app.schemas.schemas import Pagination, LeaderboardEntry
from app.utils.query_helpers import get_stat_domains, get_available_stats_for_domain

router = APIRouter(prefix="/api/dl/stats", tags=["deadlocked-stats"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/leaderboard/{domain}/{stat}")
def deadlocked_leaderboard(domain: str, stat: str, page: int = 1, session: Session = Depends(get_db)) -> Pagination[LeaderboardEntry]:
    """
    Generate a paginated leaderboard (100 entries per page) for all Deadlocked stats. `domain` is a game mode or
    collection of stats (e.g., conquest, ctf, weapon, vehicle, etc.) and `stat` is a field that belongs to the parent
    stat domain. All domains and all stats are formatted in snake case.
    """
    stat_domains: dict[str, type[DeclarativeBase]] = get_stat_domains()

    if domain not in stat_domains:
        raise HTTPException(status_code=400, detail=f"Invalid stat domain '{domain}'.")

    stat_domain: type[DeclarativeBase] = stat_domains[domain]
    available_stats: list[str] = get_available_stats_for_domain(stat_domain)

    if stat not in available_stats:
        raise HTTPException(status_code=400, detail=f"Invalid stat field '{stat}'.")

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

    return Pagination[LeaderboardEntry](
        count=count,
        results=[
            LeaderboardEntry(
                horizon_id=result.horizon_id,
                username=result.username,
                score=score,
                rank=(100 * page) + index + 1
            )
            for index, (result, score)
            in enumerate(results)
        ]
    )