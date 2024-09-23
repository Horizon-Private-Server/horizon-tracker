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
from horizon.middleware_manager import dl_online_tracker as online_tracker

router = APIRouter(prefix="/api/dl/online", tags=["dl-online"])

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
    games: list[DeadlockedGameOnlineSchema] = online_tracker.get_games()
    return Pagination[DeadlockedGameOnlineSchema](count=len(games), results=games)

