from cachetools import cached, TTLCache
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import column, func

from sqlalchemy.orm import Session, Query, DeclarativeBase

from app.database import SessionLocal
from app.models.uya import UyaPlayer

from app.schemas.schemas import (
    Pagination,
    LeaderboardEntry,
    StatOffering,
    UyaSiegeStatsSchema,
    UyaDeathmatchStatsSchema,
    UyaOverallStatsSchema,
    UyaCTFStatsSchema,
    UyaPlayerDetailsSchema,
    PlayerSchema
)
from app.utils.query_helpers import get_stat_domains, get_available_stats_for_domain, uya_compute_stat_offerings

from fuzzywuzzy import fuzz


router = APIRouter(prefix="/api/uya/stats", tags=["uya-stats"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/offerings")
def uya_stat_offerings() -> Pagination[StatOffering]:
    """
    Provides a list of all stat offerings tracked by Horizon. These offerings include the appropriate domain, stat and
    label for requesting leaderboard data.
    """
    offerings = uya_compute_stat_offerings()
    return Pagination[StatOffering](count=len(offerings), results=offerings)


@router.get("/leaderboard/{domain}/{stat}")
def uya_leaderboard(domain: str, stat: str, page: int = 1, session: Session = Depends(get_db)) -> Pagination[LeaderboardEntry]:
    """
    Generate a paginated leaderboard (100 entries per page) for all Deadlocked stats. `domain` is a game mode or
    collection of stats (e.g., conquest, ctf, weapon, vehicle, etc.) and `stat` is a field that belongs to the parent
    stat domain. All domains and all stats are formatted in snake case.
    """
    stat_domains: dict[str, type[DeclarativeBase]] = get_stat_domains("uya")

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

    query: Query = session.query(UyaPlayer) \
        .join(stat_domain) \
        .add_columns(column(stat)) \
        .order_by(getattr(stat_domain, stat).desc(), UyaPlayer.id.asc())

    results: list[tuple[UyaPlayer, int]] = list(query.offset(100 * page).limit(100))

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
def uya_player(id: int, session: Session = Depends(get_db)) -> UyaPlayerDetailsSchema:
    """
    Generate a paginated leaderboard (100 entries per page) for all Deadlocked stats. `domain` is a game mode or
    collection of stats (e.g., conquest, ctf, weapon, vehicle, etc.) and `stat` is a field that belongs to the parent
    stat domain. All domains and all stats are formatted in snake case.
    """

    query: Query = session.query(UyaPlayer).filter_by(id=id)

    stat_domains: dict[str, type[DeclarativeBase]] = get_stat_domains("uya")
    for domain in stat_domains:
        stat_domain: type[DeclarativeBase] = stat_domains[domain]
        query = query.join(stat_domain)


    result: UyaPlayer = query.first()

    if result is None:
        raise HTTPException(status_code=404, detail=f"Player with ID '{id}' not found.")

    stat_schema_dictionary: dict[str, type[BaseModel]] = {
        "overall_stats": UyaOverallStatsSchema,
        "deathmatch_stats": UyaDeathmatchStatsSchema,
        "siege_stats": UyaSiegeStatsSchema,
        "ctf_stats": UyaCTFStatsSchema,
    }

    # TODO This is a very convoluted one-liner, add better documentation.
    return UyaPlayerDetailsSchema(
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


@cached(cache=TTLCache(maxsize=5, ttl=3600), key=lambda _: 0)
def get_all_uya_players(session: Session) -> list[PlayerSchema]:
    return [
        PlayerSchema(id=result.id, username=result.username)
        for result
        in session.query(UyaPlayer).with_entities(UyaPlayer.id, UyaPlayer.username)
    ]

@router.get("/search")
def player_search(q: str, page: int, session: Session = Depends(get_db)) -> Pagination[PlayerSchema]:
    """
    Generate a paginated player lookup (100 entries per page) for all Deadlocked players. `q` is a query
    to look up a player by username. `page` is the page lookup page. Each page consists of 100 entries.
    """

    if q.strip() == "":
        return Pagination[PlayerSchema](count=0, results=[])

    # Deadlocked and UYA accounts have a max length of 16. Since Levenshtein distance has performance impacts
    # with increased string lengths, truncate excess characters. This will prevent potential DOS attacks using
    # long query strings to overload compute performance.
    q = q[:16]

    if page < 1:
        page = 0
    else:
        page -= 1

    all_players: list[PlayerSchema] = get_all_uya_players(session)

    results: list[PlayerSchema] = list(sorted(all_players, key=lambda result: fuzz.ratio(result.username.lower(), q.lower()), reverse=True))

    return Pagination[PlayerSchema](
        count=len(results),
        results=[
            PlayerSchema(id=player.id, username=player.username)
            for player
            in results[page * 100: (page + 1) * 100]
        ]
    )
