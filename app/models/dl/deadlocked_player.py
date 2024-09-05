from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


# Vanilla Stats

class DeadlockedOverallStats(Base):
    __tablename__ = "deadlocked_overall_stats"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    player = relationship("DeadlockedPlayer", uselist=False, back_populates="overall_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    disconnects = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    squats = Column(Integer, default=0, nullable=False)


class DeadlockedDeathmatchStats(Base):
    __tablename__ = "deadlocked_deathmatch_stats"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    player = relationship("DeadlockedPlayer", uselist=False, back_populates="deathmatch_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)


class DeadlockedConquestStats(Base):
    __tablename__ = "deadlocked_conquest_stats"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    player = relationship("DeadlockedPlayer", uselist=False, back_populates="conquest_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    nodes_taken = Column(Integer, default=0, nullable=False)


class DeadlockedCTFStats(Base):
    __tablename__ = "deadlocked_ctf_stats"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    player = relationship("DeadlockedPlayer", uselist=False, back_populates="ctf_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    flags_captured = Column(Integer, default=0, nullable=False)


class DeadlockedKOTHStats(Base):
    __tablename__ = "deadlocked_koth_stats"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    player = relationship("DeadlockedPlayer", uselist=False, back_populates="koth_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    time = Column(Integer, default=0, nullable=False)


class DeadlockedJuggernautStats(Base):
    __tablename__ = "deadlocked_juggernaut_stats"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    player = relationship("DeadlockedPlayer", uselist=False, back_populates="juggernaut_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    time = Column(Integer, default=0, nullable=False)


class DeadlockedWeaponStats(Base):
    __tablename__ = "deadlocked_weapon_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="weapon_stats")

    wrench_kills = Column(Integer, default=0, nullable=False)
    wrench_deaths = Column(Integer, default=0, nullable=False)
    dual_viper_kills = Column(Integer, default=0, nullable=False)
    dual_viper_deaths = Column(Integer, default=0, nullable=False)
    magma_cannon_kills = Column(Integer, default=0, nullable=False)
    magma_cannon_deaths = Column(Integer, default=0, nullable=False)
    arbiter_kills = Column(Integer, default=0, nullable=False)
    arbiter_deaths = Column(Integer, default=0, nullable=False)
    fusion_rifle_kills = Column(Integer, default=0, nullable=False)
    fusion_rifle_deaths = Column(Integer, default=0, nullable=False)
    hunter_mine_launcher_kills = Column(Integer, default=0, nullable=False)
    hunter_mine_launcher_deaths = Column(Integer, default=0, nullable=False)
    b6_obliterator_kills = Column(Integer, default=0, nullable=False)
    b6_obliterator_deaths = Column(Integer, default=0, nullable=False)
    scorpion_flail_kills = Column(Integer, default=0, nullable=False)
    scorpion_flail_deaths = Column(Integer, default=0, nullable=False)
    holoshield_launcher_kills = Column(Integer, default=0, nullable=False)
    holoshield_launcher_deaths = Column(Integer, default=0, nullable=False)


class DeadlockedVehicleStats(Base):
    __tablename__ = "deadlocked_vehicle_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="vehicle_stats")

    roadkills = Column(Integer, default=0, nullable=False)
    squats = Column(Integer, default=0, nullable=False)

# Custom Stats
# TODO

# Deadlocked Player


class DeadlockedPlayer(Base):
    __tablename__ = "deadlocked_player"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    horizon_id = Column(Integer, index=True, unique=True, nullable=False)

    # TODO This should have a unique constraint, but there are duplicates in the Horizon Prod data.
    # TODO Wait for a Prod stats cleanup.
    username = Column(String, nullable=False)

    overall_stats = relationship("DeadlockedOverallStats", uselist=False, back_populates="player", cascade="all, delete")
    deathmatch_stats = relationship("DeadlockedDeathmatchStats", uselist=False, back_populates="player", cascade="all, delete")
    conquest_stats = relationship("DeadlockedConquestStats", uselist=False, back_populates="player", cascade="all, delete")
    ctf_stats = relationship("DeadlockedCTFStats", uselist=False, back_populates="player", cascade="all, delete")
    koth_stats = relationship("DeadlockedKOTHStats", uselist=False, back_populates="player", cascade="all, delete")
    juggernaut_stats = relationship("DeadlockedJuggernautStats", uselist=False, back_populates="player", cascade="all, delete")
    weapon_stats = relationship("DeadlockedWeaponStats", uselist=False, back_populates="player", cascade="all, delete")
    vehicle_stats = relationship("DeadlockedVehicleStats", uselist=False, back_populates="player", cascade="all, delete")

    def __init__(self, *args, **kwargs):
        super(DeadlockedPlayer, self).__init__(*args, **kwargs)

        self.overall_stats = DeadlockedOverallStats()
        self.deathmatch_stats = DeadlockedDeathmatchStats()
        self.conquest_stats = DeadlockedConquestStats()
        self.ctf_stats = DeadlockedCTFStats()
        self.koth_stats = DeadlockedKOTHStats()
        self.juggernaut_stats = DeadlockedJuggernautStats()
        self.weapon_stats = DeadlockedWeaponStats()
        self.vehicle_stats = DeadlockedVehicleStats()
