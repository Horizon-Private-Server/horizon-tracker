from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


# Vanilla Stats

class DeadlockedOverallStats(Base):
    __tablename__ = "deadlocked_overall_stats"

    id = Column(Integer, primary_key=True, index=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="overall_stats")

    rank = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    disconnects = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    games_played = Column(Integer)
    squats = Column(Integer)


class DeadlockedDeathmatchStats(Base):
    __tablename__ = "deadlocked_deathmatch_stats"

    id = Column(Integer, primary_key=True, index=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="deathmatch_stats")

    rank = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)


class DeadlockedConquestStats(Base):
    __tablename__ = "deadlocked_conquest_stats"

    id = Column(Integer, primary_key=True, index=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="conquest_stats")

    rank = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    nodes_taken = Column(Integer)


class DeadlockedCTFStats(Base):
    __tablename__ = "deadlocked_ctf_stats"

    id = Column(Integer, primary_key=True, index=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="ctf_stats")

    rank = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    flags_captured = Column(Integer)


class DeadlockedKOTHStats(Base):
    __tablename__ = "deadlocked_koth_stats"

    id = Column(Integer, primary_key=True, index=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="koth_stats")

    rank = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    hill_time = Column(Integer)


class DeadlockedJuggernautStats(Base):
    __tablename__ = "deadlocked_juggernaut_stats"

    id = Column(Integer, primary_key=True, index=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="juggernaut_stats")

    rank = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    juggernaut_time = Column(Integer)


class DeadlockedWeaponStats(Base):
    __tablename__ = "deadlocked_weapon_stats"

    id = Column(Integer, primary_key=True, index=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="weapon_stats")

    wrench_kills = Column(Integer)
    wrench_deaths = Column(Integer)
    dual_viper_kills = Column(Integer)
    dual_viper_deaths = Column(Integer)
    magma_cannon_kills = Column(Integer)
    magma_cannon_deaths = Column(Integer)
    arbiter_kills = Column(Integer)
    arbiter_deaths = Column(Integer)
    fusion_rifle_kills = Column(Integer)
    fusion_rifle_deaths = Column(Integer)
    hunter_mine_launcher_kills = Column(Integer)
    hunter_mine_launcher_deaths = Column(Integer)
    b6_obliterator_kills = Column(Integer)
    b6_obliterator_deaths = Column(Integer)
    scorpion_flail_kills = Column(Integer)
    scorpion_flail_deaths = Column(Integer)


class DeadlockedVehicleStats(Base):
    __tablename__ = "deadlocked_vehicle_stats"

    id = Column(Integer, primary_key=True, index=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="vehicle_stats")

    roadkills = Column(Integer)
    squats = Column(Integer)

# Custom Stats
# TODO

# Deadlocked Player


class DeadlockedPlayer(Base):
    __tablename__ = "deadlocked_player"

    id = Column(Integer, primary_key=True, index=True)
    horizon_id = Column(Integer, index=True)

    overall_stats = relationship("DeadlockedOverallStats", uselist=False, back_populates="player")
    deathmatch_stats = relationship("DeadlockedDeathmatchStats", uselist=False, back_populates="player")
    conquest_stats = relationship("DeadlockedConquestStats", uselist=False, back_populates="player")
    ctf_stats = relationship("DeadlockedCTFStats", uselist=False, back_populates="player")
    koth_stats = relationship("DeadlockedKOTHStats", uselist=False, back_populates="player")
    juggernaut_stats = relationship("DeadlockedJuggernautStats", uselist=False, back_populates="player")
    weapon_stats = relationship("DeadlockedWeaponStats", uselist=False, back_populates="player")
    vehicle_stats = relationship("DeadlockedVehicleStats", uselist=False, back_populates="player")
