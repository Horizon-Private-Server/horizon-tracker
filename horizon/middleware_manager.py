import asyncio
from copy import deepcopy
import json
from datetime import datetime

from app.database import CREDENTIALS
from horizon.middleware_api import get_players_online, authenticate_async, authenticate, get_active_games
from horizon.parsing.uya_game import uya_map_parser, uya_time_parser, uya_gamemode_parser

from app.schemas.schemas import (
    Pagination,
    UyaPlayerOnlineSchema,
    UyaGameOnlineSchema,
    DeadlockedPlayerOnlineSchema,
    DeadlockedGameOnlineSchema,
)


class MiddlewareManager:
    def __init__(self, game:str, players_online_poll_interval:int=60, token_poll_interval:int=3600):
        """
        Class to manager all middleware calls and polling.

        :param players_online_poll_interval: Interval time in seconds to poll the players online API
        :param token_poll_interval: Interval time in seconds to refresh the token
        """
        self._players_online_poll_interval = players_online_poll_interval
        self._token_poll_interval = token_poll_interval
        self._players_online = []
        self._games_online = []

        self._protocol: str = CREDENTIALS[game]["horizon_middleware_protocol"]
        self._host: str = CREDENTIALS[game]["horizon_middleware_host"]
        self._horizon_app_id: int = CREDENTIALS[game]["horizon_app_id"]
        self._horizon_username: str = CREDENTIALS[game]["horizon_middleware_username"]
        self._horizon_password: str = CREDENTIALS[game]["horizon_middleware_password"]

        self._token: str = authenticate(
            protocol=self._protocol,
            host=self._host,
            username=self._horizon_username,
            password=self._horizon_password
        )

    async def refresh_token(self) -> None:
        # Periodically refresh token so we don't get 401
        while True:
            self._token = await authenticate_async(
                protocol=self._protocol,
                host=self._host,
                username=self._horizon_username,
                password=self._horizon_password
            )
            await asyncio.sleep(self._token_poll_interval)

    async def poll_players_online(self) -> None:
        # Poll forever and update internal variable
        while True:
            self._players_online: list[dict] = await get_players_online(self._protocol, self._host, self._token)
            self._games_online: list[dict] = await get_active_games(self._protocol, self._host, self._token)

            await asyncio.sleep(self._players_online_poll_interval)


class UyaOnlineTracker(MiddlewareManager):
    def __init__(self, players_online_poll_interval:int=60, token_poll_interval:int=3600):
        super().__init__("uya", players_online_poll_interval, token_poll_interval)

    def get_players(self) -> list[UyaPlayerOnlineSchema]:
        players_online = [
            UyaPlayerOnlineSchema(
                username=player['AccountName']
            ) for player in self._players_online
        ]
        return deepcopy(players_online)

    def get_games(self) -> list[UyaGameOnlineSchema]:
        games = []

        # Process each game
        for game in self._games_online:
            game_metadata = json.loads(game["Metadata"]) if game["Metadata"] else None
            game_players = list(filter(lambda x: x["GameId"] is not None and x["GameId"] == game["GameId"], self._players_online))

            if game_metadata is not None and game_metadata["CustomMap"] is not None:
                map = game_metadata["CustomMap"]
            else:
                map = uya_map_parser(game['GenericField3'])

            game_mode, game_type = uya_gamemode_parser(game['GenericField3'])

            timelimit = uya_time_parser(game['GenericField3'])

            games.append(UyaGameOnlineSchema(
                name=game['GameName'][0:15].strip(),
                game_status=game["WorldStatus"],
                map=map,
                time_started=game["GameStartDt"][:26] if game["WorldStatus"] == 'WorldActive' and game["GameStartDt"] is not None else 'Not yet started',
                time_limit=timelimit,
                game_mode=game_mode,
                game_type=game_type,
                last_updated=str(datetime.now()),
                players=[UyaPlayerOnlineSchema(username=player['AccountName']) for player in game_players]
            ))

        return deepcopy(games)



class DeadlockedOnlineTracker(MiddlewareManager):
    def __init__(self, players_online_poll_interval:int=60, token_poll_interval:int=3600):
        super().__init__("dl", players_online_poll_interval, token_poll_interval)

    def get_players(self) -> list[DeadlockedPlayerOnlineSchema]:
        players = [
            DeadlockedPlayerOnlineSchema(
                username=player['AccountName']
            ) for player in self._players_online
        ]
        return deepcopy(players)
    

    def get_games(self) -> list[DeadlockedGameOnlineSchema]:
        games = []

        # Process each game
        for game in self._games_online:
            game_players = list(filter(lambda x: x["GameId"] is not None and x["GameId"] == game["GameId"], self._players_online))

            games.append(DeadlockedGameOnlineSchema(
                name=game['GameName'][0:15].strip(),
                game_status=game["WorldStatus"],
                time_started=game["GameStartDt"][:26] if game["WorldStatus"] == 'WorldActive' and game["GameStartDt"] is not None else 'Not yet started',
                last_updated=str(datetime.now()),
                players=[DeadlockedPlayerOnlineSchema(username=player['AccountName']) for player in game_players]
            ))

        return deepcopy(games)




uya_online_tracker = UyaOnlineTracker()
dl_online_tracker = DeadlockedOnlineTracker()