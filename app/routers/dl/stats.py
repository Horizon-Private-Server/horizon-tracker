from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import column

from sqlalchemy.orm import Session, Query, DeclarativeBase

from app.database import SessionLocal
from app.models.dl import DeadlockedPlayer

from app.schemas.schemas import (
    Pagination,
    LeaderboardEntry,
    StatOffering,
    DeadlockedPlayerDetailsSchema,
    DeadlockedOverallStatsSchema,
    DeadlockedDeathmatchStatsSchema,
    DeadlockedConquestStatsSchema,
    DeadlockedCTFStatsSchema,
    DeadlockedGameModeWithTimeSchema,
    DeadlockedWeaponStatsSchema, DeadlockedVehicleStatsSchema
)
from app.utils.query_helpers import get_stat_domains, get_available_stats_for_domain, compute_stat_offerings

router = APIRouter(prefix="/api/dl/stats", tags=["deadlocked-stats"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/offerings")
def deadlocked_stat_offerings() -> Pagination[StatOffering]:
    """
    Provides a list of all stat offerings tracked by Horizon. These offerings include the appropriate domain, stat and
    label for requesting leaderboard data.
    """
    offerings = compute_stat_offerings()
    return Pagination[StatOffering](count=len(offerings), results=offerings)


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
        page = 0
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

@router.get("/player/{horizon_id}")
def deadlocked_leaderboard(horizon_id: int, session: Session = Depends(get_db)) -> DeadlockedPlayerDetailsSchema:
    """
    Generate a paginated leaderboard (100 entries per page) for all Deadlocked stats. `domain` is a game mode or
    collection of stats (e.g., conquest, ctf, weapon, vehicle, etc.) and `stat` is a field that belongs to the parent
    stat domain. All domains and all stats are formatted in snake case.
    """

    query: Query = session.query(DeadlockedPlayer).filter_by(horizon_id=horizon_id)

    stat_domains: dict[str, type[DeclarativeBase]] = get_stat_domains()
    for domain in stat_domains:
        stat_domain: type[DeclarativeBase] = stat_domains[domain]
        query = query.join(stat_domain)


    result: DeadlockedPlayer = query.first()

    # TODO See if this can be compressed into a 1-liner that won't require future maintenance.
    return DeadlockedPlayerDetailsSchema(
        horizon_id=result.horizon_id,
        username=result.username,
        overall_stats=DeadlockedOverallStatsSchema(
            **{field: getattr(result.overall_stats, field) for field in result.overall_stats.__dict__}
        ),
        deathmatch_stats=DeadlockedDeathmatchStatsSchema(
            **{field: getattr(result.deathmatch_stats, field) for field in result.deathmatch_stats.__dict__}
        ),
        conquest_stats = DeadlockedConquestStatsSchema(
            **{field: getattr(result.conquest_stats, field) for field in result.conquest_stats.__dict__}
        ),
        ctf_stats=DeadlockedCTFStatsSchema(
            **{field: getattr(result.ctf_stats, field) for field in result.ctf_stats.__dict__}
        ),
        koth_stats = DeadlockedGameModeWithTimeSchema(
            **{field: getattr(result.koth_stats, field) for field in result.koth_stats.__dict__}
        ),
        juggernaut_stats = DeadlockedGameModeWithTimeSchema(
            **{field: getattr(result.juggernaut_stats, field) for field in result.juggernaut_stats.__dict__}
        ),
        weapon_stats=DeadlockedWeaponStatsSchema(
            **{field: getattr(result.weapon_stats, field) for field in result.weapon_stats.__dict__}
        ),
        vehicle_stats=DeadlockedVehicleStatsSchema(
            **{field: getattr(result.vehicle_stats, field) for field in result.vehicle_stats.__dict__}
        )
    )