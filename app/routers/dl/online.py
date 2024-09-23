import copy
import asyncio
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import column

from sqlalchemy.orm import Session, Query, DeclarativeBase

from app.database import SessionLocal
from app.schemas.schemas import (
    Pagination,
    DeadlockedPlayerOnlineSchema,
    DeadlockedGameOnlineSchema,
)

from app.database import CREDENTIALS
from horizon.middleware_api import get_players_online, get_active_games, authenticate_async, authenticate

class DeadlockedOnlineTracker:
    def __init__(self):
        self._poll_interval = 60 # Every minute
        self._token_poll_interval = 60 * 60 # Every hour
        self._players_online = []
        self._games_online = []

        self._protocol: str = CREDENTIALS["dl"]["horizon_middleware_protocol"]
        self._host: str = CREDENTIALS["dl"]["horizon_middleware_host"]
        self._horizon_app_id: int = CREDENTIALS["dl"]["horizon_app_id"]
        self._horizon_username: str = CREDENTIALS["dl"]["horizon_middleware_username"]
        self._horizon_password: str = CREDENTIALS["dl"]["horizon_middleware_password"]

        self._token: str = authenticate(
            protocol=self._protocol,
            host=self._host,
            username=self._horizon_username,
            password=self._horizon_password
        )

    def get_players(self) -> list[DeadlockedPlayerOnlineSchema]:
        return copy.deepcopy(self._players_online)

    def get_games(self) -> list[DeadlockedGameOnlineSchema]:
        return copy.deepcopy(self._games_online)


    async def poll_forever(self) -> None:
        # Poll forever and update internal variable
        while True:
            players_online: list[dict] = await get_players_online(self._protocol, self._host, self._token)
            games_online: list[dict] = await get_active_games(self._protocol, self._host, self._token)

            self._players_online = [
                DeadlockedPlayerOnlineSchema(
                    username=player['AccountName']
                ) for player in players_online
            ]

            self._games_online = []

            # Process each game
            for game in games_online:
                game_players = list(filter(lambda x: x["GameId"] is not None and x["GameId"] == game["GameId"], players_online))

                self._games_online.append(DeadlockedGameOnlineSchema(
                    name=game['GameName'][0:15].strip(),
                    game_status=game["WorldStatus"],
                    time_started=game["GameStartDt"][:26] if game["WorldStatus"] == 'WorldActive' and game["GameStartDt"] is not None else 'Not yet started',
                    last_updated=str(datetime.now()),
                    players=[DeadlockedPlayerOnlineSchema(username=player['AccountName']) for player in game_players]
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

router = APIRouter(prefix="/api/dl/online", tags=["dl-online"])

online_tracker = DeadlockedOnlineTracker()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/players")
def dl_players_online() -> Pagination[DeadlockedPlayerOnlineSchema]:
    """
    Provide a list of players who are currently online.
    """
    players: list[DeadlockedPlayerOnlineSchema] = online_tracker.get_players()
    return Pagination[DeadlockedPlayerOnlineSchema](count=len(players), results=players)


@router.get("/games")
def dl_games_online() -> Pagination[DeadlockedGameOnlineSchema]:
    """
    Provide a list of games currently being played.
    """
    players: list[DeadlockedGameOnlineSchema] = online_tracker.get_games()
    return Pagination[DeadlockedGameOnlineSchema](count=len(players), results=players)

