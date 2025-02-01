import asyncio
from copy import deepcopy
import json
from datetime import datetime
import logging
from tabulate import tabulate
import requests

from app.database import (
    CREDENTIALS,
    SessionLocalAsync
)
from app.utils.query_helpers import (
    update_player_vanilla_stats_async,
    update_uya_gamehistory_async,
    check_uya_gamehistory_exists_async,
    get_uya_gamehistory_and_player_stats_async,
    get_uya_player_name_async
)
from horizon.middleware_api import (
    get_players_online, 
    authenticate_async, 
    authenticate, 
    get_active_games,
    get_recent_stats,
    get_recent_game_history
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
    def __init__(self, players_online_poll_interval:int=60, token_poll_interval:int=3600, recent_stats_poll_interval:int=120, recent_games_poll_interval:int=120):
        """
        Class to manager all middleware calls and polling.

        :param players_online_poll_interval: Interval time in seconds to poll the players online API
        :param token_poll_interval: Interval time in seconds to refresh the token
        """
        self._players_online_poll_interval = players_online_poll_interval
        self._token_poll_interval = token_poll_interval
        self._recent_stats_poll_interval = recent_stats_poll_interval
        self._recent_games_poll_interval = recent_games_poll_interval
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
            game_metadata = json.loads(game["Metadata"]) if "Metadata" in game.keys() and game["Metadata"] else {}
            game_players = list(filter(lambda _player: _player["GameId"] is not None and _player["GameId"] == game["GameId"], self._players_online))

            if "CustomMap" in game_metadata.keys() and game_metadata["CustomMap"] != None:
                map = game_metadata["CustomMap"]
            else:
                map = uya_map_parser(game["GenericField3"], game_metadata)

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
                logger.error("[uya] refresh_token failed to update!", exc_info=True)

            await asyncio.sleep(self._token_poll_interval)

    async def poll_active_online(self) -> None:
        # Poll forever and update internal variable
        while True:
            # Try except so that if the db goes down, it will work when the db comes back online
            try:
                self._players_online: list[dict] = await get_players_online(self._protocol, self._host, self._token)
                self._games_online: list[dict] = await get_active_games(self._protocol, self._host, self._token)
            except Exception as e:
                logger.error("[uya] poll_active_online failed to update!", exc_info=True)

            await asyncio.sleep(self._players_online_poll_interval)

    async def update_recent_stat_changes(self) -> None:
        while True:
            # Try except so that if the db goes down, it will work when the db comes back online
            try:
                # API will return all accounts and their stats when they had a stat change in the past 5 minutes (max 60 minutes ago)
                recent_stats: list[dict] = await get_recent_stats(self._protocol, self._host, self._token)
                #logger.debug(f"[uya] update_live_stats: RECENT STATS: {recent_stats}")

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
                            logger.debug(f"[uya] update_live_stats: updating {horizon_account_id}, {stats}")
                            await update_player_vanilla_stats_async("uya", session, horizon_account_id, stats, self._protocol, self._host, self._horizon_app_id, self._token)
            except Exception as e:
                logger.error("[uya] update_recent_stat_changes failed to update!", exc_info=True)

            await asyncio.sleep(self._recent_stats_poll_interval)


    async def update_recent_game_history(self) -> None:
        while True:
            # Try except so that if the db goes down, it will work when the db comes back online
            try:
                # API will return all accounts and games that are recently ended
                recent_games: list[dict] = await get_recent_game_history(self._protocol, self._host, self._token, self._horizon_app_id)
                #logger.debug(f"[uya] update_live_stats: RECENT GAMES: {recent_games}")
                if len(recent_games) > 0:
                    async with SessionLocalAsync() as session:
                        for recent_game in recent_games:
                            logger.debug(f"[uya] update_recent_game_history: updating {recent_game}")

                            # Check if game exists in DB
                            # if it doesn't, we want to wait for the below command to finish, and then post webhook
                            #await self.post_webhook(recent_game, session)

                            if await check_uya_gamehistory_exists_async(deepcopy(recent_game), session):
                                continue
                            else:
                                await update_uya_gamehistory_async(deepcopy(recent_game), session)
                                # Post webhook
                                await self.post_webhook(recent_game, session)
            except Exception as e:
                logger.error("[uya] update_recent_game_history failed to update!", exc_info=True)

            await asyncio.sleep(self._recent_games_poll_interval)
    
    async def post_webhook(self, recent_game, session):
        gamehistory, playerstats = await get_uya_gamehistory_and_player_stats_async(deepcopy(recent_game), session)

        # Don't post webhook 
        if len(playerstats) <= 1:
            return

        playerfull = []
        for player in playerstats:
            # Get their username
            this_player = {"username": "UNKNOWN", "stats": player}
            this_player["username"] = await get_uya_player_name_async(player.player_id, session)
            this_player["username"] = this_player["username"][:7]
            if this_player["username"].startswith("CPU-"):
                return
            playerfull.append(this_player)

        red_color = 16711680
        green_color = 65280
        blue_color = 255

        color_map = {
            'CTF': blue_color,
            'Siege': red_color,
            'Deathmatch': green_color,
        }

        map = gamehistory.game_map

        if gamehistory.game_mode not in color_map:
            color = green_color
        else:
            color = color_map[gamehistory.game_mode]

        webhook_url = CREDENTIALS["uya"]["game_history_webhook_url"]
        
        str_to_post = f'```\nTime Limit: {gamehistory.time_limit}\nGame Duration: {gamehistory.game_duration:.2f} minutes\n\n'

        ### Add win/loss
        data = []
        for player in playerfull:
            data.append([player["username"], 'Win' if player["stats"].win else 'Loss'])
        data = list(sorted(data, key=lambda x: '0' + x[0] if x[1] == 'Win' else '1' + x[0]))
        data.insert(0, ["Player", "Win?"])

        tabulate_format = 'colalign'

        str_to_post += tabulate(data, headers="firstrow", tablefmt=tabulate_format)

        ### Add K/D
        data = []
        for player in playerfull:
            data.append([player["username"], 'Win' if player["stats"].win else 'Loss', player["stats"].kills, player["stats"].deaths])
        data = list(sorted(data, key=lambda x: '0' + x[0] if x[1] == 'Win' else '1' + x[0]))
        for d in data:
            d.pop(1)
        data.insert(0, ["Player", "K", "D"])

        str_to_post += '\n\n' + tabulate(data, headers="firstrow", tablefmt=tabulate_format)

        ### Add Caps/BD
        data = []
        if gamehistory.game_mode == 'CTF':
            for player in playerfull:
                data.append([player["username"], 'Win' if player["stats"].win else 'Loss', player["stats"].base_dmg, player["stats"].flag_captures])
            data = list(sorted(data, key=lambda x: '0' + x[0] if x[1] == 'Win' else '1' + x[0]))

            for d in data:
                d.pop(1)
            data.insert(0, ["Player", "BD", "Fl"])
            str_to_post += '\n\n' + tabulate(data, headers="firstrow", tablefmt=tabulate_format)

        elif gamehistory.game_mode == 'Siege':
            for player in playerfull:
                data.append([player["username"], 'Win' if player["stats"].win else 'Loss', player["stats"].base_dmg, player["stats"].nodes])
            data = list(sorted(data, key=lambda x: '0' + x[0] if x[1] == 'Win' else '1' + x[0]))

            for d in data:
                d.pop(1)
            data.insert(0, ["Player", "BD", "Nodes"])
            str_to_post += '\n\n' + tabulate(data, headers="firstrow", tablefmt=tabulate_format)

        ### End
        str_to_post += f'```\nFor more info on this game visit: https://rac-horizon.com/uya/game-history/{gamehistory.id}'

        # Define the payload
        payload = {
            # "content": f"```\n{formatted_table}\n```",
            "username": "UYA Game Scores",  # Optional: Set a custom username
            "embeds": [  # Optional: Add an embed message
                {
                    "title": f"{gamehistory.game_name} - {gamehistory.game_mode}@{map}",
                    "description": f"\n{str_to_post}\n",
                    "color": color,
                }
            ]
        }

        # Send a POST request
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()  # Raise an error for bad HTTP status codes
            print(f"Webhook delivered successfully! Status code: {response.status_code}")
            print("Response:", response.text)
        except requests.exceptions.RequestException as e:
            print(f"Failed to deliver webhook: {e}")



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
                logger.error("[dl] refresh_token failed to update!", exc_info=True)

            await asyncio.sleep(self._token_poll_interval)

    async def poll_active_online(self) -> None:
        # Poll forever and update internal variable
        while True:
            try:
                self._players_online: list[dict] = await get_players_online(self._protocol, self._host, self._token)
                self._games_online: list[dict] = await get_active_games(self._protocol, self._host, self._token)
            except Exception as e:
                logger.error("[dl] poll_active_online failed to update!", exc_info=True)

            await asyncio.sleep(self._players_online_poll_interval)

    async def update_recent_stat_changes(self) -> None:
        while True:
            try:
                # API will return all accounts and their stats when they had a stat change in the past 5 minutes (max 60 minutes ago)
                recent_stats: list[dict] = await get_recent_stats(self._protocol, self._host, self._token)
                #logger.debug(f"[dl] update_live_stats: RECENT STATS: {recent_stats}")

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
                            logger.debug(f"[dl] update_live_stats: updating {horizon_account_id}, {stats}")
                            await update_player_vanilla_stats_async("dl", session, horizon_account_id, stats, self._protocol, self._host, self._horizon_app_id, self._token)
            except Exception as e:
                logger.error("[dl] update_recent_stat_changes failed to update!", exc_info=True)

            await asyncio.sleep(self._recent_stats_poll_interval)


uya_online_tracker = UyaOnlineTracker()
dl_online_tracker = DeadlockedOnlineTracker()