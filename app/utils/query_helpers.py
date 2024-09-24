import functools
from typing import Optional
import logging

from sqlalchemy.future import select
from sqlalchemy import literal_column, func, inspect
from sqlalchemy.orm import Session, Query, DeclarativeBase, selectinload

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

from app.models.uya import (
    UyaPlayer,
    UyaOverallStats,
    UyaWeaponStats,
    UyaSiegeStats,
    UyaDeathmatchStats,
    UyaCTFStats
)

from app.schemas.schemas import StatOffering
from horizon.parsing.deadlocked_stats import vanilla_stats_map, custom_stats_map
from horizon.parsing.uya_stats import uya_vanilla_stats_map
from horizon.middleware_api import get_account_basic_stats_async

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def update_player_vanilla_stats(
    game: str,
    session: Session,
    player_id: int | str,
    player_name: str,
    wide_stats: list[int]
) -> None:
    
    if game == 'dl':
        player_class = DeadlockedPlayer
        stats_map = vanilla_stats_map
    elif game == 'uya':
        player_class = UyaPlayer
        stats_map = uya_vanilla_stats_map

    assert len(wide_stats) == 100, "The provided wide stats length is not 100, please validate your input."

    player = session.query(player_class).filter_by(horizon_id=int(player_id)).first()

    if player is None:
        player = player_class(username=player_name, horizon_id=player_id)
        session.add(player)
        session.commit()

        # TODO This has a lot of code smell, but it's a simple way to ensure the existence of 1-1 tables.
        update_player_vanilla_stats(game, session, player_id, player_name, wide_stats)
    else:

        for index, stat in enumerate(wide_stats):

            if stats_map[index]["table"] == "" or stats_map[index]["field"] == "":
                continue

            stats_table_obj: type[DeclarativeBase] = getattr(player, stats_map[index]["table"])
            setattr(stats_table_obj, stats_map[index]["field"], stat)

        session.add(player)
        session.commit()


async def update_player_vanilla_stats_async(
    game: str,
    session: Session,
    player_id: int | str,
    wide_stats: list[int],
    protocol: str,
    host: str,
    app_id: str,
    token: str,
) -> None:
    if game == 'dl':
        player_class = DeadlockedPlayer
        stats_map = vanilla_stats_map
    elif game == 'uya':
        player_class = UyaPlayer
        stats_map = uya_vanilla_stats_map

    assert len(wide_stats) == 100, "The provided wide stats length is not 100, please validate your input."

    # Need to add these to options to prevent lazy loading which fails with async
    mapper = inspect(player_class)
    options = []

    # Dynamically add selectinload for each relationship
    for rel in mapper.relationships:
        relationship_attribute = getattr(player_class, rel.key)
        options.append(selectinload(relationship_attribute))

    logger.debug(f"update_player_vanilla_stats_async: {player_id} Got options: {options}")
    # Create a select statement with the filter condition
    stmt = select(player_class).options(*options).filter_by(horizon_id=int(player_id))
    # Execute the statement asynchronously
    result = await session.execute(stmt)
    # Fetch the first result
    player = result.scalars().first()

    logger.debug(f"update_player_vanilla_stats_async: Got player: {player}")

    if player is None: # Player doesn't exist in db. Add it
        player_info: dict = await get_account_basic_stats_async(protocol, host, player_id, app_id, token)

        if player_info == {}:
            logger.warning(f"update_player_vanilla_stats_async: No information found in prod db querying: {protocol}://{host} {player_id}, {app_id}")
            return
        logger.debug(f"update_player_vanilla_stats_async: Creating user: {player_id} {player_info['AccountName']}")

        player = player_class(username=player_info["AccountName"], horizon_id=player_id)
        session.add(player)
        await session.flush()
        await session.commit()

        # TODO This has a lot of code smell, but it's a simple way to ensure the existence of 1-1 tables.
        await update_player_vanilla_stats_async(game, session, player_id, wide_stats, protocol, host, app_id, token)
    else: # Player exists in DB. Update stats
        logger.debug(f"update_player_vanilla_stats_async: User exists: {player_id}")
        for index, stat in enumerate(wide_stats):

            if stats_map[index]["table"] == "" or stats_map[index]["field"] == "":
                continue

            stats_table_obj: type[DeclarativeBase] = getattr(player, stats_map[index]["table"])
            setattr(stats_table_obj, stats_map[index]["field"], stat)

        session.add(player)
        await session.commit()



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
def get_stat_domains(game: str) -> dict[str, type[DeclarativeBase]]:
    stat_domain_dict: dict = {
        "dl": {
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
        },
        "uya": {
            "overall": UyaOverallStats,
            "deathmatch": UyaDeathmatchStats,
            "siege": UyaSiegeStats,
            "ctf": UyaCTFStats,
            "weapon": UyaWeaponStats,
        }
    }
    
    return stat_domain_dict[game]

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
def dl_compute_stat_offerings() -> list[StatOffering]:
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


@functools.cache
def uya_compute_stat_offerings() -> list[StatOffering]:
    offerings: list[StatOffering] = list()

    for stat_map in uya_vanilla_stats_map:
        stat = uya_vanilla_stats_map[stat_map]

        if any(stat[_key] == "" for _key in stat):
            continue

        offerings.append(StatOffering(
            domain=stat["table"].replace("_stats", ""),
            stat=stat["field"],
            label=stat["label"],
            custom=False
        ))

    return offerings
