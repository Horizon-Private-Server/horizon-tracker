from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import column

from sqlalchemy.orm import Session, Query, DeclarativeBase

from app.database import SessionLocal
from app.models.uya import UyaGameHistory

from app.schemas.schemas import (
    Pagination,
    UyaGameHistoryEntry
)
from app.utils.query_helpers import get_stat_domains, get_available_stats_for_domain, uya_compute_stat_offerings

router = APIRouter(prefix="/api/uya/gamehistory", tags=["uya-gamehistory"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/history")
def uya_game(page: int = 1, session: Session = Depends(get_db)) -> Pagination[UyaGameHistoryEntry]:
    """
    Generate a paginated leaderboard (100 entries per page) for all Deadlocked stats. `domain` is a game mode or
    collection of stats (e.g., conquest, ctf, weapon, vehicle, etc.) and `stat` is a field that belongs to the parent
    stat domain. All domains and all stats are formatted in snake case.
    """
    if page < 1:
        page = 0
    else:
        page -= 1

    query: Query = session.query(UyaGameHistory) \
        .order_by(UyaGameHistory.game_end_time.desc())

    results: list[tuple[UyaGameHistory, int]] = list(query.offset(100 * page).limit(100))

    count = query.count()

    return Pagination[UyaGameHistoryEntry](
        count=count,
        results=[
            UyaGameHistoryEntry(
                status=result.status,
                game_map=result.game_map,
                game_name=result.game_name,
                game_mode=result.game_mode,
                game_submode=result.game_submode,
                time_limit=result.time_limit,
                n60_enabled=result.n60_enabled,
                lava_gun_enabled=result.lava_gun_enabled,
                gravity_bomb_enabled=result.gravity_bomb_enabled,
                flux_rifle_enabled=result.flux_rifle_enabled,
                min_glove_enabled=result.min_glove_enabled,
                morph_enabled=result.morph_enabled,
                blitz_enabled=result.blitz_enabled,
                rocket_enabled=result.rocket_enabled,
                game_create_time=result.game_create_time,
                game_start_time=result.game_start_time,
                game_end_time=result.game_end_time,
                game_duration=result.game_duration
            )
            for index, (result, score)
            in enumerate(results)
        ]
    )

# class UyaGameHistory(Base):
#     __tablename__ = "uya_game_history"
#     id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)

#     status = Column(String, default="UNKNOWN STATUS", nullable=False)
#     game_map = Column(String, default="UNKNOWN GAMEMAP", nullable=False)
#     game_name = Column(String, default="UNKNOWN GAMENAME", nullable=False)
#     game_mode = Column(String, default="UNKNOWN GAMEMODE", nullable=False)
#     game_submode = Column(String, default="UNKNOWN SUBMODE", nullable=False)
#     time_limit = Column(Integer, default=0, nullable=False)
#     n60_enabled = Column(Boolean, default=False, nullable=False)
#     lava_gun_enabled = Column(Boolean, default=False, nullable=False)
#     gravity_bomb_enabled = Column(Boolean, default=False, nullable=False)
#     flux_rifle_enabled = Column(Boolean, default=False, nullable=False)
#     min_glove_enabled = Column(Boolean, default=False, nullable=False)
#     morph_enabled = Column(Boolean, default=False, nullable=False)
#     blitz_enabled = Column(Boolean, default=False, nullable=False)
#     rocket_enabled = Column(Boolean, default=False, nullable=False)

#     game_create_time = Column(DateTime, nullable=False)
#     game_start_time = Column(DateTime, nullable=False)
#     game_end_time = Column(DateTime, nullable=False)
#     game_duration = Column(Float, default=0, nullable=False) # In minutes

#     players = relationship("UyaPlayerGameStats", back_populates="game", cascade="all, delete")

# class UyaGameHistoryEntry(BaseModel):
#     status: str
#     game_map: str
#     game_name: str
#     game_mode: str
#     game_submode: str
#     time_limit: int
#     n60_enabled: bool
#     lava_gun_enabled: bool
#     gravity_bomb_enabled: bool
#     flux_rifle_enabled: bool
#     min_glove_enabled: bool
#     morph_enabled: bool
#     blitz_enabled: bool
#     rocket_enabled: bool
#     game_create_time: datetime
#     game_start_time: datetime
#     game_end_time: datetime
#     game_duration: int



# @router.get("/player/{id}")
# def uya_player(id: int, session: Session = Depends(get_db)) -> UyaPlayerDetailsSchema:
#     """
#     Generate a paginated leaderboard (100 entries per page) for all Deadlocked stats. `domain` is a game mode or
#     collection of stats (e.g., conquest, ctf, weapon, vehicle, etc.) and `stat` is a field that belongs to the parent
#     stat domain. All domains and all stats are formatted in snake case.
#     """

#     query: Query = session.query(UyaPlayer).filter_by(id=id)

#     stat_domains: dict[str, type[DeclarativeBase]] = get_stat_domains("uya")
#     for domain in stat_domains:
#         stat_domain: type[DeclarativeBase] = stat_domains[domain]
#         query = query.join(stat_domain)


#     result: UyaPlayer = query.first()

#     if result is None:
#         raise HTTPException(status_code=404, detail=f"Player with ID '{id}' not found.")

#     stat_schema_dictionary: dict[str, type[BaseModel]] = {
#         "overall_stats": UyaOverallStatsSchema,
#         "deathmatch_stats": UyaDeathmatchStatsSchema,
#         "siege_stats": UyaSiegeStatsSchema,
#         "ctf_stats": UyaCTFStatsSchema,
#     }

#     # TODO This is a very convoluted one-liner, add better documentation.
#     return UyaPlayerDetailsSchema(
#         id=result.id,
#         username=result.username,
#         **{
#             stat_schema_key: stat_schema_dictionary[stat_schema_key](
#                 **{
#                     field: getattr(getattr(result, stat_schema_key), field)
#                     for field
#                     in getattr(result, stat_schema_key).__dict__
#                 }
#             )
#             for stat_schema_key
#             in stat_schema_dictionary
#         }
#     )
