import functools
from typing import Optional
from datetime import datetime
import json
import logging


from sqlalchemy.future import select
from sqlalchemy import literal_column, func, inspect
from sqlalchemy.orm import Session, Query, DeclarativeBase, selectinload

from app.utils.database import retry_async

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
    UyaCTFStats,
    UyaGameHistory,
    UyaPlayerGameStats,
)


from app.schemas.schemas import StatOffering
from horizon.parsing.deadlocked_stats import vanilla_stats_map, custom_stats_map
from horizon.parsing.uya_stats import uya_vanilla_stats_map

from horizon.parsing.uya_game import (
    uya_map_parser, 
    uya_time_parser, 
    uya_gamemode_parser,
    uya_game_name_parser,
    uya_weapon_parser
)

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
    
    if game == "dl":
        player_class = DeadlockedPlayer
        stats_map = vanilla_stats_map
    elif game == "uya":
        player_class = UyaPlayer
        stats_map = uya_vanilla_stats_map

    assert len(wide_stats) == 100, "The provided wide stats length is not 100, please validate your input."

    player = session.query(player_class).filter_by(id=int(player_id)).first()

    if player is None:
        player = player_class(username=player_name, id=player_id)
        session.add(player)
        session.commit()

        # TODO This has a lot of code smell, but it"s a simple way to ensure the existence of 1-1 tables.
        update_player_vanilla_stats(game, session, player_id, player_name, wide_stats)
    else:

        for index, stat in enumerate(wide_stats):

            if stats_map[index]["table"] == "" or stats_map[index]["field"] == "":
                continue

            stats_table_obj: type[DeclarativeBase] = getattr(player, stats_map[index]["table"])
            setattr(stats_table_obj, stats_map[index]["field"], stat)

        session.add(player)
        session.commit()

@retry_async(retries=3, delay=2)
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

    #logger.debug(f"update_player_vanilla_stats_async: {player_id} Got options: {options}")
    # Create a select statement with the filter condition
    stmt = select(player_class).options(*options).filter_by(id=int(player_id))
    # Execute the statement asynchronously
    result = await session.execute(stmt)
    # Fetch the first result
    player = result.scalars().first()

    #logger.debug(f"update_player_vanilla_stats_async: Got player: {player}")

    if player is None: # Player doesn't exist in db. Add it
        player_info: dict = await get_account_basic_stats_async(protocol, host, player_id, app_id, token)

        if player_info == {}:
            logger.warning(f"update_player_vanilla_stats_async: No information found in prod db querying: {protocol}://{host} {player_id}, {app_id}")
            return
        logger.debug(f"update_player_vanilla_stats_async: Creating user: {player_id} {player_info['AccountName']}")

        player = player_class(username=player_info["AccountName"], id=player_id)
        session.add(player)
        await session.flush()
        await session.commit()

        # TODO This has a lot of code smell, but it's a simple way to ensure the existence of 1-1 tables.
        await update_player_vanilla_stats_async(game, session, player_id, wide_stats, protocol, host, app_id, token)
    else: # Player exists in DB. Update stats
        #logger.debug(f"update_player_vanilla_stats_async: User exists: {player_id}")
        for index, stat in enumerate(wide_stats):

            if stats_map[index]["table"] == "" or stats_map[index]["field"] == "":
                continue

            stats_table_obj: type[DeclarativeBase] = getattr(player, stats_map[index]["table"])
            setattr(stats_table_obj, stats_map[index]["field"], stat)

        session.add(player)
        await session.commit()


@retry_async(retries=3, delay=2)
async def get_uya_player_name_async(
    player_id: int | str,
    session: Session,
) -> None:
    # Need to add these to options to prevent lazy loading which fails with async
    mapper = inspect(UyaPlayer)
    options = []

    # Dynamically add selectinload for each relationship
    for rel in mapper.relationships:
        relationship_attribute = getattr(UyaPlayer, rel.key)
        options.append(selectinload(relationship_attribute))

    #logger.debug(f"update_player_vanilla_stats_async: {player_id} Got options: {options}")
    # Create a select statement with the filter condition
    stmt = select(UyaPlayer).options(*options).filter_by(id=int(player_id))
    # Execute the statement asynchronously
    result = await session.execute(stmt)
    # Fetch the first result
    player = result.scalars().first()

    if player:
        return player.username
    else:
        return 'UNKNOWN'




def update_uya_gamehistory(
    game: dict,
    session: Session
) -> None:

    if "Metadata" not in game.keys() or game["Metadata"] == None:
        game["Metadata"] = {}
    else:
        game["Metadata"] = json.loads(game["Metadata"])

    # Get player count
    if "PreWideStats" in game["Metadata"].keys() and "Players" in game["Metadata"]["PreWideStats"].keys():
        player_count:int = len(game["Metadata"]["PreWideStats"]["Players"])
    else:
        player_count = 0

    # Check if a record already exists
    existing_game = session.query(UyaGameHistory).filter_by(id=int(game["Id"])).first()

    if existing_game:
        # Update the existing record
        existing_game.status = game["WorldStatus"]
        existing_game.game_map = uya_map_parser(game["GenericField3"], game["Metadata"])
        existing_game.game_name = uya_game_name_parser(game["GameName"])
        existing_game.game_mode = uya_gamemode_parser(game["GenericField3"])[0]
        existing_game.game_submode = uya_gamemode_parser(game["GenericField3"])[1]
        existing_game.time_limit = uya_time_parser(game["GenericField3"])
        existing_game.n60_enabled = uya_weapon_parser(game["PlayerSkillLevel"])["N60"]
        existing_game.lava_gun_enabled = uya_weapon_parser(game["PlayerSkillLevel"])["Lava Gun"]
        existing_game.gravity_bomb_enabled = uya_weapon_parser(game["PlayerSkillLevel"])["Gravity Bomb"]
        existing_game.flux_rifle_enabled = uya_weapon_parser(game["PlayerSkillLevel"])["Flux Rifle"]
        existing_game.mine_glove_enabled = uya_weapon_parser(game["PlayerSkillLevel"])["Mine Glove"]
        existing_game.morph_enabled = uya_weapon_parser(game["PlayerSkillLevel"])["Morph O' Ray"]
        existing_game.blitz_enabled = uya_weapon_parser(game["PlayerSkillLevel"])["Blitz Cannon"]
        existing_game.rocket_enabled = uya_weapon_parser(game["PlayerSkillLevel"])["Rocket"]
        existing_game.player_count = player_count
        existing_game.game_create_time = datetime.fromisoformat(game["GameCreateDt"][:26])
        existing_game.game_start_time = datetime.fromisoformat(game["GameStartDt"][:26])
        existing_game.game_end_time = datetime.fromisoformat(game["GameEndDt"][:26])
        existing_game.game_duration = (datetime.fromisoformat(game["GameEndDt"][:26]) - datetime.fromisoformat(game["GameStartDt"][:26])).total_seconds() / 60
    else:
        # Create a new record
        new_game_model = UyaGameHistory(
            id=int(game["Id"]),
            status=game["WorldStatus"],
            game_map=uya_map_parser(game["GenericField3"], game["Metadata"]),
            game_name=uya_game_name_parser(game["GameName"]),
            game_mode=uya_gamemode_parser(game["GenericField3"])[0],
            game_submode=uya_gamemode_parser(game["GenericField3"])[1],
            time_limit=uya_time_parser(game["GenericField3"]),
            n60_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["N60"],
            lava_gun_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Lava Gun"],
            gravity_bomb_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Gravity Bomb"],
            flux_rifle_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Flux Rifle"],
            mine_glove_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Mine Glove"],
            morph_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Morph O' Ray"],
            blitz_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Blitz Cannon"],
            rocket_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Rocket"],
            player_count=player_count,
            game_create_time=datetime.fromisoformat(game["GameCreateDt"][:26]),
            game_start_time=datetime.fromisoformat(game["GameStartDt"][:26]),
            game_end_time=datetime.fromisoformat(game["GameEndDt"][:26]),
            game_duration=(datetime.fromisoformat(game["GameEndDt"][:26]) - datetime.fromisoformat(game["GameStartDt"][:26])).total_seconds() / 60
        )
        session.add(new_game_model)

    session.flush()
    session.commit()

    # Clean PostWideStats - PreWideStats for each player
    if "PreWideStats" in game["Metadata"].keys() and "Players" in game["Metadata"]["PreWideStats"].keys():
        players_pre: list[str] = [horizon_account_id for horizon_account_id in game["Metadata"]["PreWideStats"]["Players"]]

        # Subtract players post from players pre
        for horizon_player_id in players_pre:
            stat_difference:list = [post_stat - pre_stat for post_stat, pre_stat in zip(game["Metadata"]["PostWideStats"]["Players"][horizon_player_id], game["Metadata"]["PreWideStats"]["Players"][horizon_player_id])]

            if stat_difference == []:
                continue
            # Convert stat difference to string key
            player_cleaned_stats:dict[str, int] = {uya_vanilla_stats_map[key]['label']: value for key, value in zip(uya_vanilla_stats_map.keys(), stat_difference) if uya_vanilla_stats_map[key]["label"]}

            existing_player_game_stats = session.query(UyaPlayerGameStats).filter_by(game_id=int(game["Id"])).filter_by(player_id=int(horizon_player_id)).first()
            if existing_player_game_stats:
                    existing_player_game_stats.win = player_cleaned_stats["Wins"] == 1 # If there was +1 to win stat
                    existing_player_game_stats.kills = player_cleaned_stats["Kills"]
                    existing_player_game_stats.deaths = player_cleaned_stats["Deaths"]
                    existing_player_game_stats.base_dmg = player_cleaned_stats["Total Base Damage"]
                    existing_player_game_stats.flag_captures = player_cleaned_stats["CTF Flags Captured"]
                    existing_player_game_stats.flag_saves = player_cleaned_stats["CTF Flags Saved"]
                    existing_player_game_stats.suicides = player_cleaned_stats["Suicides"]
                    existing_player_game_stats.nodes = player_cleaned_stats["Total Nodes"]
                    existing_player_game_stats.n60_deaths = player_cleaned_stats["N60 Deaths"]
                    existing_player_game_stats.n60_kills = player_cleaned_stats["N60 Kills"]
                    existing_player_game_stats.lava_gun_deaths = player_cleaned_stats["Lava Gun Deaths"]
                    existing_player_game_stats.lava_gun_kills = player_cleaned_stats["Lava Gun Kills"]
                    existing_player_game_stats.gravity_bomb_deaths = player_cleaned_stats["Gravity Bomb Deaths"]
                    existing_player_game_stats.gravity_bomb_kills = player_cleaned_stats["Gravity Bomb Kills"]
                    existing_player_game_stats.flux_rifle_deaths = player_cleaned_stats["Flux Rifle Deaths"]
                    existing_player_game_stats.flux_rifle_kills = player_cleaned_stats["Flux Rifle Kills"]
                    existing_player_game_stats.mine_glove_deaths = player_cleaned_stats["Mine Glove Deaths"]
                    existing_player_game_stats.mine_glove_kills = player_cleaned_stats["Mine Glove Kills"]
                    existing_player_game_stats.morph_deaths = player_cleaned_stats["Morph-O-Ray Deaths"]
                    existing_player_game_stats.morph_kills = player_cleaned_stats["Morph-O-Ray Kills"]
                    existing_player_game_stats.blitz_deaths = player_cleaned_stats["Blitz Cannon Deaths"]
                    existing_player_game_stats.blitz_kills = player_cleaned_stats["Blitz Cannon Kills"]
                    existing_player_game_stats.rocket_deaths = player_cleaned_stats["Rocket Deaths"]
                    existing_player_game_stats.rocket_kills = player_cleaned_stats["Rocket Kills"]
                    existing_player_game_stats.wrench_deaths = player_cleaned_stats["Wrench Deaths"]
                    existing_player_game_stats.wrench_kills = player_cleaned_stats["Wrench Kills"]
            else:
                players_game_stats = UyaPlayerGameStats(
                    game_id = int(game["Id"]),
                    player_id = int(horizon_player_id),

                    win = player_cleaned_stats["Wins"] == 1, # If there was +1 to win stat
                    kills = player_cleaned_stats["Kills"],
                    deaths = player_cleaned_stats["Deaths"],
                    base_dmg = player_cleaned_stats["Total Base Damage"],
                    flag_captures = player_cleaned_stats["CTF Flags Captured"],
                    flag_saves = player_cleaned_stats["CTF Flags Saved"],
                    suicides = player_cleaned_stats["Suicides"],
                    nodes = player_cleaned_stats["Total Nodes"],
                    n60_deaths = player_cleaned_stats["N60 Deaths"],
                    n60_kills = player_cleaned_stats["N60 Kills"],
                    lava_gun_deaths = player_cleaned_stats["Lava Gun Deaths"],
                    lava_gun_kills = player_cleaned_stats["Lava Gun Kills"],
                    gravity_bomb_deaths = player_cleaned_stats["Gravity Bomb Deaths"],
                    gravity_bomb_kills = player_cleaned_stats["Gravity Bomb Kills"],
                    flux_rifle_deaths = player_cleaned_stats["Flux Rifle Deaths"],
                    flux_rifle_kills = player_cleaned_stats["Flux Rifle Kills"],
                    mine_glove_deaths = player_cleaned_stats["Mine Glove Deaths"],
                    mine_glove_kills = player_cleaned_stats["Mine Glove Kills"],
                    morph_deaths = player_cleaned_stats["Morph-O-Ray Deaths"],
                    morph_kills = player_cleaned_stats["Morph-O-Ray Kills"],
                    blitz_deaths = player_cleaned_stats["Blitz Cannon Deaths"],
                    blitz_kills = player_cleaned_stats["Blitz Cannon Kills"],
                    rocket_deaths = player_cleaned_stats["Rocket Deaths"],
                    rocket_kills = player_cleaned_stats["Rocket Kills"],
                    wrench_deaths = player_cleaned_stats["Wrench Deaths"],
                    wrench_kills = player_cleaned_stats["Wrench Kills"],
                )
                session.add(players_game_stats)

    # Commit the changes
    session.commit()


@retry_async(retries=3, delay=2)
async def get_uya_gamehistory_and_player_stats_async(
    game: dict,
    session: Session
) -> None:
    # Need to add these to options to prevent lazy loading which fails with async
    mapper = inspect(UyaGameHistory)
    options = []

    # Dynamically add selectinload for each relationship
    for rel in mapper.relationships:
        relationship_attribute = getattr(UyaGameHistory, rel.key)
        options.append(selectinload(relationship_attribute))

    #logger.debug(f"update_player_vanilla_stats_async: {player_id} Got options: {options}")
    # Create a select statement with the filter condition
    stmt = select(UyaGameHistory).options(*options).filter_by(id=int(game["Id"]))
    # Execute the statement asynchronously
    result = await session.execute(stmt)
    # Fetch the first result
    game_result = result.scalars().first()

    mapper = inspect(UyaPlayerGameStats)
    options = []

    # Dynamically add selectinload for each relationship
    for rel in mapper.relationships:
        relationship_attribute = getattr(UyaPlayerGameStats, rel.key)
        options.append(selectinload(relationship_attribute))
    stmt = select(UyaPlayerGameStats).options(*options).filter_by(game_id=int(game["Id"]))
    existing_player_game_stats = await session.execute(stmt)
    existing_player_game_stats = existing_player_game_stats.scalars().all()
    return game_result, existing_player_game_stats

@retry_async(retries=3, delay=2)
async def check_uya_gamehistory_exists_async(
    game: dict,
    session: Session
) -> None:
    # Need to add these to options to prevent lazy loading which fails with async
    mapper = inspect(UyaGameHistory)
    options = []

    # Dynamically add selectinload for each relationship
    for rel in mapper.relationships:
        relationship_attribute = getattr(UyaGameHistory, rel.key)
        options.append(selectinload(relationship_attribute))

    #logger.debug(f"update_player_vanilla_stats_async: {player_id} Got options: {options}")
    # Create a select statement with the filter condition
    stmt = select(UyaGameHistory).options(*options).filter_by(id=int(game["Id"]))
    # Execute the statement asynchronously
    result = await session.execute(stmt)
    # Fetch the first result
    game_result = result.scalars().first()

    return game_result is not None



@retry_async(retries=3, delay=2)
async def update_uya_gamehistory_async(
    game: dict,
    session: Session
) -> None:

    if "Metadata" not in game.keys() or game["Metadata"] == None or game["Metadata"] == {}:
        game["Metadata"] = {}
    elif type(game["Metadata"]) == str:
        game["Metadata"] = json.loads(game["Metadata"])

    # Get player count
    if "PreWideStats" in game["Metadata"].keys() and "Players" in game["Metadata"]["PreWideStats"].keys():
        player_count:int = len(game["Metadata"]["PreWideStats"]["Players"])
    else:
        player_count = 0

    # Need to add these to options to prevent lazy loading which fails with async
    mapper = inspect(UyaGameHistory)
    options = []

    # Dynamically add selectinload for each relationship
    for rel in mapper.relationships:
        relationship_attribute = getattr(UyaGameHistory, rel.key)
        options.append(selectinload(relationship_attribute))

    #logger.debug(f"update_player_vanilla_stats_async: {player_id} Got options: {options}")
    # Create a select statement with the filter condition
    stmt = select(UyaGameHistory).options(*options).filter_by(id=int(game["Id"]))
    # Execute the statement asynchronously
    result = await session.execute(stmt)
    # Fetch the first result
    game_result = result.scalars().first()

    if game_result is None: # Game doesn't exist in db. Add it
        logger.debug(f"update_uya_gamehistory_async: Got new game: {int(game["Id"])}")

        new_game_model = UyaGameHistory(
            id=int(game["Id"]),
            status=game["WorldStatus"],
            game_map=uya_map_parser(game["GenericField3"], game["Metadata"]),
            game_name=uya_game_name_parser(game["GameName"]),
            game_mode=uya_gamemode_parser(game["GenericField3"])[0],
            game_submode=uya_gamemode_parser(game["GenericField3"])[1],
            time_limit=uya_time_parser(game["GenericField3"]),
            n60_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["N60"],
            lava_gun_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Lava Gun"],
            gravity_bomb_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Gravity Bomb"],
            flux_rifle_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Flux Rifle"],
            mine_glove_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Mine Glove"],
            morph_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Morph O' Ray"],
            blitz_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Blitz Cannon"],
            rocket_enabled=uya_weapon_parser(game["PlayerSkillLevel"])["Rocket"],
            player_count=player_count,
            game_create_time=datetime.fromisoformat(game["GameCreateDt"][:26]),
            game_start_time=datetime.fromisoformat(game["GameStartDt"][:26]),
            game_end_time=datetime.fromisoformat(game["GameEndDt"][:26]),
            game_duration=(datetime.fromisoformat(game["GameEndDt"][:26]) - datetime.fromisoformat(game["GameStartDt"][:26])).total_seconds() / 60
        )
        session.add(new_game_model)
        await session.flush()
        await session.commit()
    else: # Update rows
        pass
        #logger.debug(f"update_uya_gamehistory_async: Already have this game: {int(game["Id"])}")


    # Need to add these to options to prevent lazy loading which fails with async
    mapper = inspect(UyaPlayerGameStats)
    options = []
    # Dynamically add selectinload for each relationship
    for rel in mapper.relationships:
        relationship_attribute = getattr(UyaPlayerGameStats, rel.key)
        options.append(selectinload(relationship_attribute))

    # Clean PostWideStats - PreWideStats for each player
    if "PreWideStats" in game["Metadata"].keys() and "Players" in game["Metadata"]["PreWideStats"].keys():
        players_pre: list[str] = [horizon_account_id for horizon_account_id in game["Metadata"]["PreWideStats"]["Players"]]

        # Subtract players post from players pre
        for horizon_player_id in players_pre:
            stat_difference:list = [post_stat - pre_stat for post_stat, pre_stat in zip(game["Metadata"]["PostWideStats"]["Players"][horizon_player_id], game["Metadata"]["PreWideStats"]["Players"][horizon_player_id])]

            # Convert stat difference to string key
            player_cleaned_stats:dict[str, int] = {uya_vanilla_stats_map[key]['label']: value for key, value in zip(uya_vanilla_stats_map.keys(), stat_difference) if uya_vanilla_stats_map[key]["label"]}

            #logger.debug(f"update_player_vanilla_stats_async: {player_id} Got options: {options}")
            # Create a select statement with the filter condition
            stmt = select(UyaPlayerGameStats).options(*options).filter_by(game_id=int(game["Id"])).filter_by(player_id=int(horizon_player_id))
            # Execute the statement asynchronously
            result = await session.execute(stmt)
            # Fetch the first result
            player_result = result.scalars().first()

            if player_result is None:
                players_game_stats = UyaPlayerGameStats(
                    game_id = int(game["Id"]),
                    player_id = int(horizon_player_id),

                    win = player_cleaned_stats["Wins"] == 1, # If there was +1 to win stat
                    kills = player_cleaned_stats["Kills"],
                    deaths = player_cleaned_stats["Deaths"],
                    base_dmg = player_cleaned_stats["Total Base Damage"],
                    flag_captures = player_cleaned_stats["CTF Flags Captured"],
                    flag_saves = player_cleaned_stats["CTF Flags Saved"],
                    suicides = player_cleaned_stats["Suicides"],
                    nodes = player_cleaned_stats["Total Nodes"],
                    n60_deaths = player_cleaned_stats["N60 Deaths"],
                    n60_kills = player_cleaned_stats["N60 Kills"],
                    lava_gun_deaths = player_cleaned_stats["Lava Gun Deaths"],
                    lava_gun_kills = player_cleaned_stats["Lava Gun Kills"],
                    gravity_bomb_deaths = player_cleaned_stats["Gravity Bomb Deaths"],
                    gravity_bomb_kills = player_cleaned_stats["Gravity Bomb Kills"],
                    flux_rifle_deaths = player_cleaned_stats["Flux Rifle Deaths"],
                    flux_rifle_kills = player_cleaned_stats["Flux Rifle Kills"],
                    mine_glove_deaths = player_cleaned_stats["Mine Glove Deaths"],
                    mine_glove_kills = player_cleaned_stats["Mine Glove Kills"],
                    morph_deaths = player_cleaned_stats["Morph-O-Ray Deaths"],
                    morph_kills = player_cleaned_stats["Morph-O-Ray Kills"],
                    blitz_deaths = player_cleaned_stats["Blitz Cannon Deaths"],
                    blitz_kills = player_cleaned_stats["Blitz Cannon Kills"],
                    rocket_deaths = player_cleaned_stats["Rocket Deaths"],
                    rocket_kills = player_cleaned_stats["Rocket Kills"],
                    wrench_deaths = player_cleaned_stats["Wrench Deaths"],
                    wrench_kills = player_cleaned_stats["Wrench Kills"],
                )
                session.add(players_game_stats)
                await session.flush()
                await session.commit()






# TODO Determine if this should be part of a single function.
# TODO There are trade-offs to keeping them separate and merging them.
def update_deadlocked_player_custom_stats(
    session: Session,
    player_id: int | str,
    player_name: str,
    wide_custom_stats: list[int]
) -> None:

    player: Optional[DeadlockedPlayer] = session.query(DeadlockedPlayer).filter_by(id=int(player_id)).first()

    if player is None:
        player = DeadlockedPlayer(username=player_name, id=player_id)
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
