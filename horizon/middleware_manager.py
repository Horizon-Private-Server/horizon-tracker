import asyncio
from copy import deepcopy
import json
from datetime import datetime
import logging

from app.database import (
    CREDENTIALS,
    SessionLocalAsync
)
from app.utils.query_helpers import update_player_vanilla_stats_async
from horizon.middleware_api import (
    get_players_online, 
    authenticate_async, 
    authenticate, 
    get_active_games,
    get_recent_stats
)
from horizon.parsing.uya_game import (
    uya_map_parser, 
    uya_time_parser, 
    uya_gamemode_parser
)
from app.schemas.schemas import (
    UyaPlayerOnlineSchema,
    UyaGameOnlineSchema,
    DeadlockedPlayerOnlineSchema,
    DeadlockedGameOnlineSchema,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

class UyaOnlineTracker:
    def __init__(self, players_online_poll_interval:int=60, token_poll_interval:int=3600, recent_stats_poll_interval:int=120):
        """
        Class to manager all middleware calls and polling.

        :param players_online_poll_interval: Interval time in seconds to poll the players online API
        :param token_poll_interval: Interval time in seconds to refresh the token
        """
        self._players_online_poll_interval = players_online_poll_interval
        self._token_poll_interval = token_poll_interval
        self._recent_stats_poll_interval = recent_stats_poll_interval
        self._players_online = []
        self._games_online = []

        self._protocol: str = CREDENTIALS["uya"]["horizon_middleware_protocol"]
        self._host: str = CREDENTIALS["uya"]["horizon_middleware_host"]
        self._horizon_app_id: int = CREDENTIALS["uya"]["horizon_app_id_ntsc"]
        self._horizon_username: str = CREDENTIALS["uya"]["horizon_middleware_username"]
        self._horizon_password: str = CREDENTIALS["uya"]["horizon_middleware_password"]

        self._token: str = authenticate(
            protocol=self._protocol,
            host=self._host,
            username=self._horizon_username,
            password=self._horizon_password
        )

    def get_players(self) -> list[UyaPlayerOnlineSchema]:
        players_online = [
            UyaPlayerOnlineSchema(
                username=player["AccountName"]
            ) for player in self._players_online
        ]
        return deepcopy(players_online)

    def get_games(self) -> list[UyaGameOnlineSchema]:
        games = []

        # Process each game
        for game in self._games_online:
            game_metadata = json.loads(game["Metadata"]) if game["Metadata"] else None
            game_players = list(filter(lambda _player: _player["GameId"] is not None and _player["GameId"] == game["GameId"], self._players_online))

            if game_metadata is not None and game_metadata["CustomMap"] is not None:
                map = game_metadata["CustomMap"]
            else:
                map = uya_map_parser(game["GenericField3"], json.loads(game["Metadata"]))

            game_mode, game_type = uya_gamemode_parser(game["GenericField3"])

            timelimit = uya_time_parser(game["GenericField3"])

            games.append(UyaGameOnlineSchema(
                id=int(game["GameId"]),
                name=game["GameName"][0:15].strip(),
                game_status=game["WorldStatus"],
                map=map,
                time_started=game["GameStartDt"][:26] if game["WorldStatus"] == "WorldActive" and game["GameStartDt"] is not None else "Not yet started",
                time_limit=timelimit,
                game_mode=game_mode,
                game_type=game_type,
                last_updated=str(datetime.now()),
                players=[UyaPlayerOnlineSchema(username=player["AccountName"]) for player in game_players]
            ))

        return deepcopy(games)

    async def refresh_token(self) -> None:
        # Periodically refresh token so we don't get 401
        while True:
            # Try except so that if the db goes down, it will work when the db comes back online
            try:
                self._token = await authenticate_async(
                    protocol=self._protocol,
                    host=self._host,
                    username=self._horizon_username,
                    password=self._horizon_password
                )
            except Exception as e:
                logger.error("refresh_token failed to update!", exc_info=True)

            await asyncio.sleep(self._token_poll_interval)

    async def poll_active_online(self) -> None:
        # Poll forever and update internal variable
        while True:
            # Try except so that if the db goes down, it will work when the db comes back online
            try:
                self._players_online: list[dict] = await get_players_online(self._protocol, self._host, self._token)
                self._games_online: list[dict] = await get_active_games(self._protocol, self._host, self._token)
            except Exception as e:
                logger.error("poll_active_online failed to update!", exc_info=True)

            await asyncio.sleep(self._players_online_poll_interval)

    async def update_recent_stat_changes(self) -> None:
        while True:
            # Try except so that if the db goes down, it will work when the db comes back online
            try:
                # API will return all accounts and their stats when they had a stat change in the past 5 minutes (max 60 minutes ago)
                recent_stats: list[dict] = await get_recent_stats(self._protocol, self._host, self._token)
                logger.debug(f"update_live_stats: RECENT STATS: {recent_stats}")

                if len(recent_stats) > 0:
                    async with SessionLocalAsync() as session:
                        for recent_stat_change in recent_stats:
                            # For each stat change that we have, update the database.
                            horizon_account_id:int = recent_stat_change["AccountId"]

                            # Convert stats dict of StatIdx:StatValue to a list
                            stats = [0] * 100
                            for stat_idx, stat_value in recent_stat_change["Stats"].items():
                                stats[int(stat_idx)-1] = stat_value

                            # Doesn't block the entire backend while updating DB with this players new stats
                            logger.debug(f"update_live_stats: updating {horizon_account_id}, {stats}")
                            await update_player_vanilla_stats_async("uya", session, horizon_account_id, stats, self._protocol, self._host, self._horizon_app_id, self._token)
            except Exception as e:
                logger.error("update_recent_stat_changes failed to update!", exc_info=True)

            await asyncio.sleep(self._recent_stats_poll_interval)


class DeadlockedOnlineTracker:
    def __init__(self, players_online_poll_interval:int=60, token_poll_interval:int=3600, recent_stats_poll_interval:int=120):
        """
        Class to manager all middleware calls and polling.

        :param players_online_poll_interval: Interval time in seconds to poll the players online API
        :param token_poll_interval: Interval time in seconds to refresh the token
        """
        self._players_online_poll_interval = players_online_poll_interval
        self._token_poll_interval = token_poll_interval
        self._recent_stats_poll_interval = recent_stats_poll_interval
        self._players_online = []
        self._games_online = []

        self._protocol: str = CREDENTIALS["dl"]["horizon_middleware_protocol"]
        self._host: str = CREDENTIALS["dl"]["horizon_middleware_host"]
        self._horizon_app_id: int = CREDENTIALS["dl"]["horizon_app_id_ntsc"]
        self._horizon_username: str = CREDENTIALS["dl"]["horizon_middleware_username"]
        self._horizon_password: str = CREDENTIALS["dl"]["horizon_middleware_password"]

        self._token: str = authenticate(
            protocol=self._protocol,
            host=self._host,
            username=self._horizon_username,
            password=self._horizon_password
        )


    def get_players(self) -> list[DeadlockedPlayerOnlineSchema]:
        players = [
            DeadlockedPlayerOnlineSchema(
                username=player["AccountName"]
            ) for player in self._players_online
        ]
        return deepcopy(players)
    

    def get_games(self) -> list[DeadlockedGameOnlineSchema]:
        games = []

        # Process each game
        for game in self._games_online:
            game_players = list(filter(lambda _player: _player["GameId"] is not None and _player["GameId"] == game["GameId"], self._players_online))

            games.append(DeadlockedGameOnlineSchema(
                name=game["GameName"][0:15].strip(),
                game_status=game["WorldStatus"],
                time_started=game["GameStartDt"][:26] if game["WorldStatus"] == "WorldActive" and game["GameStartDt"] is not None else "Not yet started",
                last_updated=str(datetime.now()),
                players=[DeadlockedPlayerOnlineSchema(username=player["AccountName"]) for player in game_players]
            ))

        return deepcopy(games)


    async def refresh_token(self) -> None:
        # Periodically refresh token so we don't get 401
        while True:
            try:
                self._token = await authenticate_async(
                    protocol=self._protocol,
                    host=self._host,
                    username=self._horizon_username,
                    password=self._horizon_password
                )
            except Exception as e:
                logger.error("refresh_token failed to update!", exc_info=True)

            await asyncio.sleep(self._token_poll_interval)

    async def poll_active_online(self) -> None:
        # Poll forever and update internal variable
        while True:
            try:
                self._players_online: list[dict] = await get_players_online(self._protocol, self._host, self._token)
                self._games_online: list[dict] = await get_active_games(self._protocol, self._host, self._token)
            except Exception as e:
                logger.error("poll_active_online failed to update!", exc_info=True)

            await asyncio.sleep(self._players_online_poll_interval)

    async def update_recent_stat_changes(self) -> None:
        while True:
            try:
                # API will return all accounts and their stats when they had a stat change in the past 5 minutes (max 60 minutes ago)
                recent_stats: list[dict] = await get_recent_stats(self._protocol, self._host, self._token)
                logger.debug(f"update_live_stats: RECENT STATS: {recent_stats}")

                if len(recent_stats) > 0:
                    async with SessionLocalAsync() as session:
                        for recent_stat_change in recent_stats:
                            # For each stat change that we have, update the database.
                            horizon_account_id:int = recent_stat_change["AccountId"]

                            # Convert stats dict of StatIdx:StatValue to a list
                            stats = [0] * 100
                            for stat_idx, stat_value in recent_stat_change["Stats"].items():
                                stats[int(stat_idx)-1] = stat_value

                            # Doesn't block the entire backend while updating DB with this players new stats
                            logger.debug(f"update_live_stats: updating {horizon_account_id}, {stats}")
                            await update_player_vanilla_stats_async("dl", session, horizon_account_id, stats, self._protocol, self._host, self._horizon_app_id, self._token)
            except Exception as e:
                logger.error("update_recent_stat_changes failed to update!", exc_info=True)

            await asyncio.sleep(self._recent_stats_poll_interval)


uya_online_tracker = UyaOnlineTracker()
dl_online_tracker = DeadlockedOnlineTracker()