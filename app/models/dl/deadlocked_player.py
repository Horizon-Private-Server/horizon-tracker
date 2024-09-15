from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


###############
# Vanilla Stats
###############
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


##############
# Custom Stats
##############
class DeadlockedHorizonStats(Base):
    __tablename__ = "deadlocked_horizon_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="horizon_stats")

    total_bolts = Column(Integer, default=0, nullable=False)
    current_bolts = Column(Integer, default=0, nullable=False)


class DeadlockedSNDStats(Base):
    __tablename__ = "deadlocked_snd_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="snd_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    plants = Column(Integer, default=0, nullable=False)
    defuses = Column(Integer, default=0, nullable=False)
    ninja_defuses = Column(Integer, default=0, nullable=False)
    wins_attacking = Column(Integer, default=0, nullable=False)
    wins_defending = Column(Integer, default=0, nullable=False)
    time_played = Column(Integer, default=0, nullable=False)


class DeadlockedPayloadStats(Base):
    __tablename__ = "deadlocked_payload_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="payload_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    points = Column(Integer, default=0, nullable=False)
    kills_while_hot = Column(Integer, default=0, nullable=False)
    kills_on_hot = Column(Integer, default=0, nullable=False)
    time_played = Column(Integer, default=0, nullable=False)


class DeadlockedSpleefStats(Base):
    __tablename__ = "deadlocked_spleef_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="spleef_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    rounds_played = Column(Integer, default=0, nullable=False)
    points = Column(Integer, default=0, nullable=False)
    time_played = Column(Integer, default=0, nullable=False)
    boxes_broken = Column(Integer, default=0, nullable=False)


class DeadlockedInfectedStats(Base):
    __tablename__ = "deadlocked_infected_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="infected_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    infections = Column(Integer, default=0, nullable=False)
    times_infected = Column(Integer, default=0, nullable=False)
    time_played = Column(Integer, default=0, nullable=False)
    wins_as_survivor = Column(Integer, default=0, nullable=False)
    wins_as_first_infected = Column(Integer, default=0, nullable=False)


class DeadlockedGungameStats(Base):
    __tablename__ = "deadlocked_gungame_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="gungame_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    demotions = Column(Integer, default=0, nullable=False)
    times_demoted = Column(Integer, default=0, nullable=False)
    promotions = Column(Integer, default=0, nullable=False)
    time_played = Column(Integer, default=0, nullable=False)


class DeadlockedInfiniteClimberStats(Base):
    __tablename__ = "deadlocked_infinite_climber_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="infinite_climber_stats")

    rank = Column(Integer, default=0, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    high_score = Column(Integer, default=0, nullable=False)
    time_played = Column(Integer, default=0, nullable=False)


class DeadlockedSurvivalStats(Base):
    __tablename__ = "deadlocked_survival_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="survival_stats")

    rank = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    time_played = Column(Integer, default=0, nullable=False)
    kills = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    revives = Column(Integer, default=0, nullable=False)
    times_revived = Column(Integer, default=0, nullable=False)

    mystery_box_rolls = Column(Integer, default=0, nullable=False)
    demon_bells_activated = Column(Integer, default=0, nullable=False)
    times_activated_power = Column(Integer, default=0, nullable=False)
    tokens_used_on_gates = Column(Integer, default=0, nullable=False)

    wrench_kills = Column(Integer, default=0, nullable=False)
    dual_viper_kills = Column(Integer, default=0, nullable=False)
    magma_cannon_kills = Column(Integer, default=0, nullable=False)
    arbiter_kills = Column(Integer, default=0, nullable=False)
    fusion_rifle_kills = Column(Integer, default=0, nullable=False)
    hunter_mine_launcher_kills = Column(Integer, default=0, nullable=False)
    b6_obliterator_kills = Column(Integer, default=0, nullable=False)
    scorpion_flail_kills = Column(Integer, default=0, nullable=False)



class DeadlockedSurvivalOrxonStats(Base):
    __tablename__ = "deadlocked_survival_orxon_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="survival_orxon_stats")

    solo_high_score = Column(Integer, default=0, nullable=False)
    coop_high_score = Column(Integer, default=0, nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    prestige = Column(Integer, default=0, nullable=False)


class DeadlockedSurvivalMountainPassStats(Base):
    __tablename__ = "deadlocked_survival_mountain_pass_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="survival_mountain_pass_stats")

    solo_high_score = Column(Integer, default=0, nullable=False)
    coop_high_score = Column(Integer, default=0, nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    prestige = Column(Integer, default=0, nullable=False)


class DeadlockedSurvivalVeldinStats(Base):
    __tablename__ = "deadlocked_survival_veldin_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="survival_veldin_stats")

    solo_high_score = Column(Integer, default=0, nullable=False)
    coop_high_score = Column(Integer, default=0, nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    prestige = Column(Integer, default=0, nullable=False)


class DeadlockedTrainingStats(Base):
    __tablename__ = "deadlocked_training_stats"

    player_id = Column(Integer, ForeignKey("deadlocked_player.id", ondelete="CASCADE"))
    id = Column(Integer, primary_key=True, index=True, unique=True)

    player = relationship("DeadlockedPlayer", uselist=False, back_populates="training_stats")

    rank = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    time_played = Column(Integer, default=0, nullable=False)
    total_kills = Column(Integer, default=0, nullable=False)

    fusion_best_points = Column(Integer, default=0, nullable=False)
    fusion_best_time = Column(Integer, default=0, nullable=False)
    fusion_kills = Column(Integer, default=0, nullable=False)
    fusion_hits = Column(Integer, default=0, nullable=False)
    fusion_misses = Column(Integer, default=0, nullable=False)
    fusion_accuracy = Column(Integer, default=0, nullable=False)
    fusion_best_combo = Column(Integer, default=0, nullable=False)

    cycle_best_points = Column(Integer, default=0, nullable=False)
    cycle_best_combo = Column(Integer, default=0, nullable=False)
    cycle_kills = Column(Integer, default=0, nullable=False)
    cycle_deaths = Column(Integer, default=0, nullable=False)
    cycle_fusion_hits = Column(Integer, default=0, nullable=False)
    cycle_fusion_misses = Column(Integer, default=0, nullable=False)
    cycle_fusion_accuracy = Column(Integer, default=0, nullable=False)


# Player table which combines all the stat tables with a 1-1 relationship.
class DeadlockedPlayer(Base):
    __tablename__ = "deadlocked_player"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    horizon_id = Column(Integer, index=True, unique=True, nullable=False)

    # TODO This should have a unique constraint, but there are duplicates in the Horizon Prod data.
    # TODO Wait for a Prod stats cleanup.
    username = Column(String, nullable=False)


    # Vanilla Stats
    overall_stats = relationship("DeadlockedOverallStats", uselist=False, back_populates="player", cascade="all, delete")
    deathmatch_stats = relationship("DeadlockedDeathmatchStats", uselist=False, back_populates="player", cascade="all, delete")
    conquest_stats = relationship("DeadlockedConquestStats", uselist=False, back_populates="player", cascade="all, delete")
    ctf_stats = relationship("DeadlockedCTFStats", uselist=False, back_populates="player", cascade="all, delete")
    koth_stats = relationship("DeadlockedKOTHStats", uselist=False, back_populates="player", cascade="all, delete")
    juggernaut_stats = relationship("DeadlockedJuggernautStats", uselist=False, back_populates="player", cascade="all, delete")
    weapon_stats = relationship("DeadlockedWeaponStats", uselist=False, back_populates="player", cascade="all, delete")
    vehicle_stats = relationship("DeadlockedVehicleStats", uselist=False, back_populates="player", cascade="all, delete")

    # Custom Stats
    horizon_stats = relationship("DeadlockedHorizonStats", uselist=False, back_populates="player", cascade="all, delete")
    snd_stats = relationship("DeadlockedSNDStats", uselist=False, back_populates="player", cascade="all, delete")
    payload_stats = relationship("DeadlockedPayloadStats", uselist=False, back_populates="player", cascade="all, delete")
    spleef_stats = relationship("DeadlockedSpleefStats", uselist=False, back_populates="player", cascade="all, delete")
    infected_stats = relationship("DeadlockedInfectedStats", uselist=False, back_populates="player", cascade="all, delete")
    gungame_stats = relationship("DeadlockedGungameStats", uselist=False, back_populates="player", cascade="all, delete")
    infinite_climber_stats = relationship("DeadlockedInfiniteClimberStats", uselist=False, back_populates="player", cascade="all, delete")
    survival_stats = relationship("DeadlockedSurvivalStats", uselist=False, back_populates="player", cascade="all, delete")
    survival_orxon_stats = relationship("DeadlockedSurvivalOrxonStats", uselist=False, back_populates="player", cascade="all, delete")
    survival_mountain_pass_stats = relationship("DeadlockedSurvivalMountainPassStats", uselist=False, back_populates="player", cascade="all, delete")
    survival_veldin_stats = relationship("DeadlockedSurvivalVeldinStats", uselist=False, back_populates="player", cascade="all, delete")
    training_stats = relationship("DeadlockedTrainingStats", uselist=False, back_populates="player", cascade="all, delete")


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

        self.horizon_stats = DeadlockedHorizonStats()
        self.snd_stats = DeadlockedSNDStats()
        self.payload_stats = DeadlockedPayloadStats()
        self.spleef_stats = DeadlockedSpleefStats()
        self.infected_stats = DeadlockedInfectedStats()
        self.gungame_stats = DeadlockedGungameStats()
        self.infinite_climber_stats = DeadlockedInfiniteClimberStats()
        self.survival_stats = DeadlockedSurvivalStats()
        self.survival_orxon_stats = DeadlockedSurvivalOrxonStats()
        self.survival_mountain_pass_stats = DeadlockedSurvivalMountainPassStats()
        self.survival_veldin_stats = DeadlockedSurvivalVeldinStats()
        self.training_stats = DeadlockedTrainingStats()
