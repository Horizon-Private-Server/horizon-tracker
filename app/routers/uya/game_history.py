from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import column

from sqlalchemy.orm import Session, Query, DeclarativeBase

from app.database import SessionLocal
from app.models.uya import (
    UyaGameHistory,
    UyaPlayerGameStats,
    UyaPlayer
)

from app.schemas.schemas import (
    Pagination,
    UyaGameHistoryEntry,
    UyaGameHistoryPlayerStatSchema,
    UyaGameHistoryDetailSchema
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
def uya_gamehistory(page: int = 1, session: Session = Depends(get_db)) -> Pagination[UyaGameHistoryEntry]:

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
                id=result.id,
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
                mine_glove_enabled=result.mine_glove_enabled,
                morph_enabled=result.morph_enabled,
                blitz_enabled=result.blitz_enabled,
                rocket_enabled=result.rocket_enabled,
                player_count=result.player_count,
                game_create_time=result.game_create_time,
                game_start_time=result.game_start_time,
                game_end_time=result.game_end_time,
                game_duration=result.game_duration
            )
            for index, result in enumerate(results)
        ]
    )



@router.get("/details/{id}")
def uya_game(id: int, session: Session = Depends(get_db)) -> None:


    query: Query = session.query(UyaGameHistory).filter_by(id=id)
    game_result: UyaGameHistory = query.first()

    if game_result is None:
        raise HTTPException(status_code=404, detail=f"Game with ID '{id}' not found.")
    
    # Get all the individual player stats
    player_query: Query = session.query(UyaPlayerGameStats, UyaPlayer.username).join(UyaPlayer, UyaPlayerGameStats.player_id == UyaPlayer.id).filter(UyaPlayerGameStats.game_id == id)
    # Tuple: UyaPlayerGameStats, username
    result: list[tuple[UyaPlayerGameStats, str]] = player_query.all()
    
    players = []
    for player_stats, username in result:
        players.append(UyaGameHistoryPlayerStatSchema(
            username=username,
            game_id = player_stats.game_id,
            player_id = player_stats.player_id,
            win = player_stats.win,
            kills = player_stats.kills,
            deaths = player_stats.deaths,
            base_dmg = player_stats.base_dmg,
            flag_captures = player_stats.flag_captures,
            flag_saves = player_stats.flag_saves,
            suicides = player_stats.suicides,
            nodes = player_stats.nodes,
            n60_deaths = player_stats.n60_deaths,
            n60_kills = player_stats.n60_kills,
            lava_gun_deaths = player_stats.lava_gun_deaths,
            lava_gun_kills = player_stats.lava_gun_kills,
            gravity_bomb_deaths = player_stats.gravity_bomb_deaths,
            gravity_bomb_kills = player_stats.gravity_bomb_kills,
            flux_rifle_deaths = player_stats.flux_rifle_deaths,
            flux_rifle_kills = player_stats.flux_rifle_kills,
            mine_glove_deaths = player_stats.mine_glove_deaths,
            mine_glove_kills = player_stats.mine_glove_kills,
            morph_deaths = player_stats.morph_deaths,
            morph_kills = player_stats.morph_kills,
            blitz_deaths = player_stats.blitz_deaths,
            blitz_kills = player_stats.blitz_kills,
            rocket_deaths = player_stats.rocket_deaths,
            rocket_kills = player_stats.rocket_kills,
            wrench_deaths = player_stats.wrench_deaths,
            wrench_kills = player_stats.wrench_kills,
        ))

    return UyaGameHistoryDetailSchema(
        game=UyaGameHistoryEntry(
            id=game_result.id,
            status=game_result.status,
            game_map=game_result.game_map,
            game_name=game_result.game_name,
            game_mode=game_result.game_mode,
            game_submode=game_result.game_submode,
            time_limit=game_result.time_limit,
            n60_enabled=game_result.n60_enabled,
            lava_gun_enabled=game_result.lava_gun_enabled,
            gravity_bomb_enabled=game_result.gravity_bomb_enabled,
            flux_rifle_enabled=game_result.flux_rifle_enabled,
            mine_glove_enabled=game_result.mine_glove_enabled,
            morph_enabled=game_result.morph_enabled,
            blitz_enabled=game_result.blitz_enabled,
            rocket_enabled=game_result.rocket_enabled,
            player_count=game_result.player_count,
            game_create_time=game_result.game_create_time,
            game_start_time=game_result.game_start_time,
            game_end_time=game_result.game_end_time,
            game_duration=game_result.game_duration
        ),
        players=players
    )
