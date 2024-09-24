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
from horizon.middleware_manager import uya_online_tracker as online_tracker

router = APIRouter(prefix="/api/uya/online", tags=["uya-online"])


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
    games: list[UyaGameOnlineSchema] = online_tracker.get_games()
    return Pagination[UyaGameOnlineSchema](count=len(games), results=games)

