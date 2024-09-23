import copy
import asyncio
from datetime import datetime
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import column

from sqlalchemy.orm import Session, Query, DeclarativeBase

from app.database import SessionLocal
from app.schemas.schemas import (
    Pagination,
    UyaPlayerOnlineSchema,
    UyaGameOnlineSchema,
)

from app.database import CREDENTIALS
from horizon.middleware_api import get_players_online, authenticate_async, authenticate, get_active_games
from horizon.parsing.uya_game import uya_map_parser, uya_time_parser, uya_gamemode_parser


class UyaOnlineTracker:
    def __init__(self):
        self._poll_interval = 60 # Every minute
        self._token_poll_interval = 60 * 60 # Every hour
        self._players_online = []
        self._games_online = {}

        self._protocol: str = CREDENTIALS["uya"]["horizon_middleware_protocol"]
        self._host: str = CREDENTIALS["uya"]["horizon_middleware_host"]
        self._horizon_app_id: int = CREDENTIALS["uya"]["horizon_app_id"]
        self._horizon_username: str = CREDENTIALS["uya"]["horizon_middleware_username"]
        self._horizon_password: str = CREDENTIALS["uya"]["horizon_middleware_password"]

        self._token: str = authenticate(
            protocol=self._protocol,
            host=self._host,
            username=self._horizon_username,
            password=self._horizon_password
        )

    def get_players(self) -> list[UyaPlayerOnlineSchema]:
        return copy.deepcopy(self._players_online)

    def get_games(self) -> list[UyaGameOnlineSchema]:
        return copy.deepcopy(self._games_online)


    async def poll_forever(self) -> None:
        # Poll forever and update internal variable
        while True:
            players_online: list[dict] = await get_players_online(self._protocol, self._host, self._token)
            games_online: list[dict] = await get_active_games(self._protocol, self._host, self._token)

            self._players_online = [
                UyaPlayerOnlineSchema(
                    username=player['AccountName']
                ) for player in players_online
            ]

            self._games_online = []

            # Process each game
            for game in games_online:
                game_metadata = json.loads(game["Metadata"]) if game["Metadata"] else None
                game_players = list(filter(lambda x: x["GameId"] is not None and x["GameId"] == game["GameId"], players_online))

                if game_metadata is not None and game_metadata["CustomMap"] is not None:
                    map = game_metadata["CustomMap"]
                else:
                    map = uya_map_parser(game['GenericField3'])

                game_mode, game_type = uya_gamemode_parser(game['GenericField3'])

                timelimit = uya_time_parser(game['GenericField3'])

                self._games_online.append(UyaGameOnlineSchema(
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

            await asyncio.sleep(self._poll_interval)

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

router = APIRouter(prefix="/api/uya/online", tags=["uya-online"])

online_tracker = UyaOnlineTracker()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/players")
def uya_players_online() -> Pagination[UyaPlayerOnlineSchema]:
    """
    Provide a list of players who are currently online.
    """
    players: list[UyaPlayerOnlineSchema] = online_tracker.get_players()
    return Pagination[UyaPlayerOnlineSchema](count=len(players), results=players)


@router.get("/games")
def uya_games_online() -> Pagination[UyaGameOnlineSchema]:
    """
    Provide a list of games currently being played.
    """
    players: list[UyaGameOnlineSchema] = online_tracker.get_games()
    return Pagination[UyaGameOnlineSchema](count=len(players), results=players)

