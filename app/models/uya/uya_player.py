from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


###############
# Vanilla Stats
###############
class UyaOverallStats(Base):
    __tablename__ = "uya_overall_stats"

    player_id = Column(Integer, ForeignKey("uya_player.id", ondelete="CASCADE"), primary_key=True, index=True, unique=True)
    player = relationship("UyaPlayer", uselist=False, back_populates="overall_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    wl_ratio = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    suicides = Column(Integer, default=0, nullable=False)
    kd_ratio = Column(Integer, default=0, nullable=False)
    base_dmg = Column(Integer, default=0, nullable=False)
    nodes = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    avg_kills = Column(Integer, default=0, nullable=False)
    avg_deaths = Column(Integer, default=0, nullable=False)
    avg_suicides = Column(Integer, default=0, nullable=False)
    avg_nodes = Column(Integer, default=0, nullable=False)
    avg_base_dmg = Column(Integer, default=0, nullable=False)
    squats = Column(Integer, default=0, nullable=False)
    avg_squats = Column(Integer, default=0, nullable=False)
    sq_ratio = Column(Integer, default=0, nullable=False)
    total_times_squatted = Column(Integer, default=0, nullable=False)
    avg_squatted_on = Column(Integer, default=0, nullable=False)
    sd_ratio = Column(Integer, default=0, nullable=False)
    total_team_squats = Column(Integer, default=0, nullable=False)
    avg_team_squats = Column(Integer, default=0, nullable=False)


class UyaDeathmatchStats(Base):
    __tablename__ = "uya_deathmatch_stats"

    player_id = Column(Integer, ForeignKey("uya_player.id", ondelete="CASCADE"), primary_key=True, index=True, unique=True)
    player = relationship("UyaPlayer", uselist=False, back_populates="deathmatch_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    wl_ratio = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    kd_ratio = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    suicides = Column(Integer, default=0, nullable=False)
    avg_kills = Column(Integer, default=0, nullable=False)
    avg_deaths = Column(Integer, default=0, nullable=False)
    avg_suicides = Column(Integer, default=0, nullable=False)


class UyaCTFStats(Base):
    __tablename__ = "uya_ctf_stats"

    player_id = Column(Integer, ForeignKey("uya_player.id", ondelete="CASCADE"), primary_key=True, index=True, unique=True)
    player = relationship("UyaPlayer", uselist=False, back_populates="ctf_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    wl_ratio = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    kd_ratio = Column(Integer, default=0, nullable=False)
    base_dmg = Column(Integer, default=0, nullable=False)
    nodes = Column(Integer, default=0, nullable=False)
    flag_captures = Column(Integer, default=0, nullable=False)
    flag_saves = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    suicides = Column(Integer, default=0, nullable=False)
    avg_kills = Column(Integer, default=0, nullable=False)
    avg_deaths = Column(Integer, default=0, nullable=False)
    avg_nodes = Column(Integer, default=0, nullable=False)
    avg_base_dmg = Column(Integer, default=0, nullable=False)
    avg_flag_captures = Column(Integer, default=0, nullable=False)
    avg_flag_saves = Column(Integer, default=0, nullable=False)
    avg_suicides = Column(Integer, default=0, nullable=False)


class UyaSiegeStats(Base):
    __tablename__ = "uya_siege_stats"

    player_id = Column(Integer, ForeignKey("uya_player.id", ondelete="CASCADE"), primary_key=True, index=True, unique=True)
    player = relationship("UyaPlayer", uselist=False, back_populates="siege_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    wl_ratio = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    kd_ratio = Column(Integer, default=0, nullable=False)
    base_dmg = Column(Integer, default=0, nullable=False)
    nodes = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    suicides = Column(Integer, default=0, nullable=False)
    avg_kills = Column(Integer, default=0, nullable=False)
    avg_deaths = Column(Integer, default=0, nullable=False)
    avg_nodes = Column(Integer, default=0, nullable=False)
    avg_base_dmg = Column(Integer, default=0, nullable=False)
    avg_suicides = Column(Integer, default=0, nullable=False)


class UyaWeaponStats(Base):
    __tablename__ = "uya_weapon_stats"

    player_id = Column(Integer, ForeignKey("uya_player.id", ondelete="CASCADE"), primary_key=True, index=True, unique=True)
    player = relationship("UyaPlayer", uselist=False, back_populates="weapon_stats")

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

# Player table which combines all the stat tables with a 1-1 relationship.
class UyaPlayer(Base):
    __tablename__ = "uya_player"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    # Note: There are duplicates in Deadlocked only because prod has both NTSC and PAL which each have their own set of usernames.
    # You can have user "test123" in NTSC, and a different account "test123" in PAL (deadlocked). UYA Shares
    # usernames across so UYA can have this unique
    username = Column(String, nullable=False, unique=True)

    # Vanilla Stats
    overall_stats = relationship("UyaOverallStats", uselist=False, back_populates="player", cascade="all, delete")
    deathmatch_stats = relationship("UyaDeathmatchStats", uselist=False, back_populates="player", cascade="all, delete")
    ctf_stats = relationship("UyaCTFStats", uselist=False, back_populates="player", cascade="all, delete")
    siege_stats = relationship("UyaSiegeStats", uselist=False, back_populates="player", cascade="all, delete")
    weapon_stats = relationship("UyaWeaponStats", uselist=False, back_populates="player", cascade="all, delete")


    def __init__(self, *args, **kwargs):
        super(UyaPlayer, self).__init__(*args, **kwargs)

        self.overall_stats = UyaOverallStats()
        self.deathmatch_stats = UyaDeathmatchStats()
        self.ctf_stats = UyaCTFStats()
        self.siege_stats = UyaSiegeStats()
        self.weapon_stats = UyaWeaponStats()