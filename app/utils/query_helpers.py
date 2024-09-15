import functools
from typing import Optional

from sqlalchemy import literal_column, func
from sqlalchemy.orm import Session, Query, DeclarativeBase

from app.models.dl import (
    DeadlockedPlayer,
    DeadlockedOverallStats,
    DeadlockedDeathmatchStats,
    DeadlockedConquestStats,
    DeadlockedCTFStats,
    DeadlockedKOTHStats,
    DeadlockedJuggernautStats,
    DeadlockedWeaponStats,
    DeadlockedVehicleStats, DeadlockedHorizonStats, DeadlockedSNDStats, DeadlockedPayloadStats, DeadlockedSpleefStats,
    DeadlockedInfectedStats, DeadlockedGungameStats, DeadlockedInfiniteClimberStats, DeadlockedSurvivalStats,
    DeadlockedSurvivalOrxonStats, DeadlockedSurvivalMountainPassStats, DeadlockedSurvivalVeldinStats,
    DeadlockedTrainingStats
)

from app.schemas.schemas import StatOffering
from horizon.parsing.deadlocked_stats import vanilla_stats_map, custom_stats_map


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

            stats_table_obj: type[DeclarativeBase] = getattr(player, vanilla_stats_map[index]["table"])
            setattr(stats_table_obj, vanilla_stats_map[index]["field"], stat)

        session.add(player)
        session.commit()


# TODO Determine if this should be part of a single function.
# TODO There are trade-offs to keeping them separate and merging them.
def update_deadlocked_player_custom_stats(
    session: Session,
    player_id: int | str,
    player_name: str,
    wide_custom_stats: list[int]
) -> None:

    player: Optional[DeadlockedPlayer] = session.query(DeadlockedPlayer).filter_by(horizon_id=int(player_id)).first()

    if player is None:
        player = DeadlockedPlayer(username=player_name, horizon_id=player_id)
        session.add(player)
        session.commit()

        # TODO Same as the TODO from the twin function.
        update_deadlocked_player_custom_stats(session, player_id, player_name, wide_custom_stats)
    else:

        for index, stat in enumerate(wide_custom_stats):

            # The custom stats map has missing entries for values that are undefined.
            if index not in custom_stats_map:
                continue

            if custom_stats_map[index]["table"] == "" or custom_stats_map[index]["field"] == "":
                continue

            stats_table_obj: type[DeclarativeBase] = getattr(player, custom_stats_map[index]["table"])
            setattr(stats_table_obj, custom_stats_map[index]["field"], stat)

        session.add(player)
        session.commit()


def query_count(query: Query) -> int:
    one_column = literal_column("1")
    counter = query.statement.with_only_columns([func.count(one_column)])
    counter = counter.order_by(None)
    return query.session.execute(counter).scalar()


@functools.cache
def get_stat_domains() -> dict[str, type[DeclarativeBase]]:
    return {
        "overall": DeadlockedOverallStats,
        "deathmatch": DeadlockedDeathmatchStats,
        "conquest": DeadlockedConquestStats,
        "ctf": DeadlockedCTFStats,
        "koth": DeadlockedKOTHStats,
        "juggernaut": DeadlockedJuggernautStats,
        "weapon": DeadlockedWeaponStats,
        "vehicle": DeadlockedVehicleStats,

        "horizon": DeadlockedHorizonStats,
        "snd": DeadlockedSNDStats,
        "payload": DeadlockedPayloadStats,
        "spleef": DeadlockedSpleefStats,
        "infected": DeadlockedInfectedStats,
        "gungame": DeadlockedGungameStats,
        "infinite_climber": DeadlockedInfiniteClimberStats,
        "survival": DeadlockedSurvivalStats,
        "survival_orxon": DeadlockedSurvivalOrxonStats,
        "survival_mountain_pass": DeadlockedSurvivalMountainPassStats,
        "survival_veldin": DeadlockedSurvivalVeldinStats,
        "training": DeadlockedTrainingStats,
    }


@functools.cache
def get_available_stats_for_domain(domain: type[DeclarativeBase]) -> list[str]:

    excess_columns = ("player", "player_id", "registry", "metadata", "id")

    return list(
        filter(
            lambda _field: not _field.startswith("_") and _field not in excess_columns,
            set(dir(DeclarativeBase)) ^ set(dir(domain))
        )
    )


@functools.cache
def compute_stat_offerings() -> list[StatOffering]:
    offerings: list[StatOffering] = list()

    for stat_map in vanilla_stats_map:
        stat = vanilla_stats_map[stat_map]

        if any(stat[_key] == "" for _key in stat):
            continue

        offerings.append(StatOffering(
            domain=stat["table"].replace("_stats", ""),
            stat=stat["field"],
            label=stat["label"],
            custom=False
        ))

    for stat_map in custom_stats_map:
        stat = custom_stats_map[stat_map]

        if any(stat[_key] == "" for _key in stat):
            continue

        offerings.append(StatOffering(
            domain=stat["table"].replace("_stats", ""),
            stat=stat["field"],
            label=stat["label"],
            custom=True
        ))

    return offerings
