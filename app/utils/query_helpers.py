import functools
from typing import Optional

from sqlalchemy import literal_column, func
from sqlalchemy.orm import Session, Query, DeclarativeBase

from app.models.dl import DeadlockedPlayer, DeadlockedOverallStats
from app.models.dl.deadlocked_player import DeadlockedWeaponStats, DeadlockedJuggernautStats, DeadlockedKOTHStats, \
    DeadlockedCTFStats, DeadlockedConquestStats, DeadlockedDeathmatchStats, DeadlockedVehicleStats
from horizon.parsing.deadlocked_stats import vanilla_stats_map


def update_deadlocked_player_vanilla_stats(
    session: Session,
    player_id: int | str,
    player_name: str,
    wide_stats: list[int]
) -> None:

    assert len(wide_stats) == 100, "The provided wide stats length is not 100, please validate your input."

    player: Optional[DeadlockedPlayer] = session.query(DeadlockedPlayer).filter_by(horizon_id=int(player_id)).first()

    if player is None:
        player = DeadlockedPlayer(username=player_name, horizon_id=player_id)
        session.add(player)
        session.commit()

        # TODO This has a lot of code smell, but it's a simple way to ensure the existence of 1-1 tables.
        update_deadlocked_player_vanilla_stats(session, player_id, player_name, wide_stats)
    else:

        for index, stat in enumerate(wide_stats):

            if vanilla_stats_map[index]["table"] == "" or vanilla_stats_map[index]["field"] == "":
                continue

            stats_table_obj = getattr(player, vanilla_stats_map[index]["table"])
            setattr(stats_table_obj, vanilla_stats_map[index]["field"], stat)

        session.add(player)
        session.commit()


def query_count(query: Query) -> int:
    one_column = literal_column("1")
    counter = query.statement.with_only_columns([func.count(one_column)])
    counter = counter.order_by(None)
    return query.session.execute(counter).scalar()


@functools.lru_cache(maxsize=None)
def get_stat_domains() -> dict[str, type[DeclarativeBase]]:
    return {
        "overall": DeadlockedOverallStats,
        "deathmatch": DeadlockedDeathmatchStats,
        "conquest": DeadlockedConquestStats,
        "ctf": DeadlockedCTFStats,
        "koth": DeadlockedKOTHStats,
        "juggernaut": DeadlockedJuggernautStats,
        "weapon": DeadlockedWeaponStats,
        "vehicle": DeadlockedVehicleStats
    }


@functools.lru_cache(maxsize=32, typed=True)
def get_available_stats_for_domain(domain: type[DeclarativeBase]) -> list[str]:

    excess_columns = ("player", "player_id", "registry", "metadata", "id")

    return list(
        filter(
            lambda _field: not _field.startswith("_") and _field not in excess_columns,
            set(dir(DeclarativeBase)) ^ set(dir(domain))
        )
    )
