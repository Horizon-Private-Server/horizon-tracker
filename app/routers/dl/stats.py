from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import column, func

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
    DeadlockedWeaponStatsSchema,
    DeadlockedVehicleStatsSchema,
    DeadlockedHorizonStatsSchema,
    DeadlockedSNDStatsSchema,
    DeadlockedPayloadStatsSchema,
    DeadlockedSpleefStatsSchema,
    DeadlockedInfectedStatsSchema,
    DeadlockedGungameStatsSchema,
    DeadlockedInfiniteClimberStatsSchema,
    DeadlockedSurvivalStatsSchema,
    DeadlockedTrainingStatsSchema,
    DeadlockedSurvivalMapStatsSchema,
    PlayerSchema
)
from app.utils.query_helpers import get_stat_domains, get_available_stats_for_domain, dl_compute_stat_offerings

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
    offerings = dl_compute_stat_offerings()
    return Pagination[StatOffering](count=len(offerings), results=offerings)


@router.get("/leaderboard/{domain}/{stat}")
def deadlocked_leaderboard(domain: str, stat: str, page: int = 1, session: Session = Depends(get_db)) -> Pagination[LeaderboardEntry]:
    """
    Generate a paginated leaderboard (100 entries per page) for all Deadlocked stats. `domain` is a game mode or
    collection of stats (e.g., conquest, ctf, weapon, vehicle, etc.) and `stat` is a field that belongs to the parent
    stat domain. All domains and all stats are formatted in snake case.
    """
    stat_domains: dict[str, type[DeclarativeBase]] = get_stat_domains("dl")

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
        .order_by(getattr(stat_domain, stat).desc(), DeadlockedPlayer.id.asc())

    results: list[tuple[DeadlockedPlayer, int]] = list(query.offset(100 * page).limit(100))

    count = query.count()

    return Pagination[LeaderboardEntry](
        count=count,
        results=[
            LeaderboardEntry(
                id=result.id,
                username=result.username,
                score=score,
                rank=(100 * page) + index + 1
            )
            for index, (result, score)
            in enumerate(results)
        ]
    )

@router.get("/player/{id}")
def deadlocked_player(id: int, session: Session = Depends(get_db)) -> DeadlockedPlayerDetailsSchema:
    """
    Generate a paginated leaderboard (100 entries per page) for all Deadlocked stats. `domain` is a game mode or
    collection of stats (e.g., conquest, ctf, weapon, vehicle, etc.) and `stat` is a field that belongs to the parent
    stat domain. All domains and all stats are formatted in snake case.
    """

    query: Query = session.query(DeadlockedPlayer).filter_by(id=id)

    stat_domains: dict[str, type[DeclarativeBase]] = get_stat_domains("dl")
    for domain in stat_domains:
        stat_domain: type[DeclarativeBase] = stat_domains[domain]
        query = query.join(stat_domain)


    result: DeadlockedPlayer = query.first()

    if result is None:
        raise HTTPException(status_code=404, detail=f"Player with ID '{id}' not found.")

    stat_schema_dictionary: dict[str, type[BaseModel]] = {
        "overall_stats": DeadlockedOverallStatsSchema,
        "deathmatch_stats": DeadlockedDeathmatchStatsSchema,
        "conquest_stats": DeadlockedConquestStatsSchema,
        "ctf_stats": DeadlockedCTFStatsSchema,
        "koth_stats": DeadlockedGameModeWithTimeSchema,
        "juggernaut_stats": DeadlockedGameModeWithTimeSchema,
        "weapon_stats": DeadlockedWeaponStatsSchema,
        "vehicle_stats": DeadlockedVehicleStatsSchema,

        "horizon_stats": DeadlockedHorizonStatsSchema,
        "snd_stats": DeadlockedSNDStatsSchema,
        "payload_stats": DeadlockedPayloadStatsSchema,
        "spleef_stats": DeadlockedSpleefStatsSchema,
        "infected_stats": DeadlockedInfectedStatsSchema,
        "gungame_stats": DeadlockedGungameStatsSchema,
        "infinite_climber_stats": DeadlockedInfiniteClimberStatsSchema,
        "survival_stats": DeadlockedSurvivalStatsSchema,
        "survival_orxon_stats": DeadlockedSurvivalMapStatsSchema,
        "survival_mountain_pass_stats": DeadlockedSurvivalMapStatsSchema,
        "survival_veldin_stats": DeadlockedSurvivalMapStatsSchema,
        "training_stats": DeadlockedTrainingStatsSchema,
    }

    # TODO This is a very convoluted one-liner, add better documentation.
    return DeadlockedPlayerDetailsSchema(
        id=result.id,
        username=result.username,
        **{
            stat_schema_key: stat_schema_dictionary[stat_schema_key](
                **{
                    field: getattr(getattr(result, stat_schema_key), field)
                    for field
                    in getattr(result, stat_schema_key).__dict__
                }
            )
            for stat_schema_key
            in stat_schema_dictionary
        }
    )


@router.get("/search")
def player_search(q: str, page: int = 1, session: Session = Depends(get_db)) -> Pagination[PlayerSchema]:
    """
    Generate a paginated player lookup (100 entries per page) for all Deadlocked players. `q` is a query
    to look up a player by username. `page` is the page lookup page. Each page consists of 100 entries.
    """

    if page < 1:
        page = 0
    else:
        page -= 1

    query: Query = session.query(
        DeadlockedPlayer).filter(DeadlockedPlayer.username.ilike(f"%{q}%") | (func.lower(DeadlockedPlayer.username) == q.lower())
    ).order_by(DeadlockedPlayer.username.asc())

    count = query.count()

    results: list[PlayerSchema] = list(query.offset(page * 100).limit(100))

    return Pagination[PlayerSchema](
        count=count,
        results=[
            PlayerSchema(id=player.id, username=player.username)
            for player
            in results
        ]
    )
