from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


###############
# Game History
###############
class UyaGameHistory(Base):
    __tablename__ = "uya_game_history"
    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)

    status = Column(String, default="UNKNOWN STATUS", nullable=False)
    game_map = Column(String, default="UNKNOWN GAMEMAP", nullable=False)
    game_name = Column(String, default="UNKNOWN GAMENAME", nullable=False)
    game_mode = Column(String, default="UNKNOWN GAMEMODE", nullable=False)
    game_submode = Column(String, default="UNKNOWN SUBMODE", nullable=False)
    time_limit = Column(Integer, default=0, nullable=False)
    n60_enabled = Column(Boolean, default=False, nullable=False)
    lava_gun_enabled = Column(Boolean, default=False, nullable=False)
    gravity_bomb_enabled = Column(Boolean, default=False, nullable=False)
    flux_rifle_enabled = Column(Boolean, default=False, nullable=False)
    min_glove_enabled = Column(Boolean, default=False, nullable=False)
    morph_enabled = Column(Boolean, default=False, nullable=False)
    blitz_enabled = Column(Boolean, default=False, nullable=False)
    rocket_enabled = Column(Boolean, default=False, nullable=False)

    game_create_time = Column(DateTime, default=False, nullable=False)
    game_start_time = Column(DateTime, default=False, nullable=False)
    game_end_time = Column(DateTime, default=False, nullable=False)
    game_duration = Column(Float, default=0, nullable=False) # In minutes

    players = relationship("UyaPlayerGameStats", back_populates="game", cascade="all, delete")


class UyaPlayerGameStats(Base):
    __tablename__ = "uya_player_game_stats"
    __table_args__ = (
        UniqueConstraint("game_id", "player_id", name="uix_game_id_player_id"),
    )

    id = Column(Integer, primary_key=True, index=True, unique=True)
    game_id = Column(Integer, ForeignKey("uya_game_history.id"), nullable=False)
    player_id = Column(Integer, nullable=False)

    win = Column(Boolean, default=False, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    base_dmg = Column(Integer, default=0, nullable=False)
    flag_captures = Column(Integer, default=0, nullable=False)
    flag_saves = Column(Integer, default=0, nullable=False)
    suicides = Column(Integer, default=0, nullable=False)
    nodes = Column(Integer, default=0, nullable=False)
    n60_deaths = Column(Integer, default=0, nullable=False)
    n60_kills = Column(Integer, default=0, nullable=False)
    lava_gun_deaths = Column(Integer, default=0, nullable=False)
    lava_gun_kills = Column(Integer, default=0, nullable=False)
    gravity_bomb_deaths = Column(Integer, default=0, nullable=False)
    gravity_bomb_kills = Column(Integer, default=0, nullable=False)
    flux_rifle_deaths = Column(Integer, default=0, nullable=False)
    flux_rifle_kills = Column(Integer, default=0, nullable=False)
    mine_glove_deaths = Column(Integer, default=0, nullable=False)
    min_glove_kills = Column(Integer, default=0, nullable=False)
    morph_deaths = Column(Integer, default=0, nullable=False)
    morph_kills = Column(Integer, default=0, nullable=False)
    blitz_deaths = Column(Integer, default=0, nullable=False)
    blitz_kills = Column(Integer, default=0, nullable=False)
    rocket_deaths = Column(Integer, default=0, nullable=False)
    rocket_kills = Column(Integer, default=0, nullable=False)
    wrench_deaths = Column(Integer, default=0, nullable=False)
    wrench_kills = Column(Integer, default=0, nullable=False)

    # Relationship back to the game
    game = relationship("UyaGameHistory", back_populates="players")
