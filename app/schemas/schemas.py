from pydantic import BaseModel


class Pagination[T](BaseModel):
    count: int
    results: list[T]


class LeaderboardEntry(BaseModel):
    horizon_id: int
    username: str
    rank: int
    score: int


class StatOffering(BaseModel):
    domain: str
    stat: str
    label: str
    custom: bool


class DeadlockedStatsBase(BaseModel):
    rank: int
    wins: int
    losses: int
    kills: int
    deaths: int


class DeadlockedOverallStatsSchema(DeadlockedStatsBase):
    games_played: int
    disconnects: int
    squats: int


class DeadlockedDeathmatchStatsSchema(DeadlockedStatsBase):
    pass


class DeadlockedConquestStatsSchema(DeadlockedStatsBase):
    nodes_taken: int


class DeadlockedCTFStatsSchema(DeadlockedStatsBase):
    flags_captured: int


class DeadlockedGameModeWithTimeSchema(DeadlockedStatsBase):
    time: int


class DeadlockedVehicleStatsSchema(BaseModel):
    roadkills: int
    squats: int


class DeadlockedWeaponStatsSchema(BaseModel):
    wrench_kills: int
    wrench_deaths: int
    dual_viper_kills: int
    dual_viper_deaths: int
    magma_cannon_kills: int
    magma_cannon_deaths: int
    arbiter_kills: int
    arbiter_deaths: int
    fusion_rifle_kills: int
    fusion_rifle_deaths: int
    hunter_mine_launcher_kills: int
    hunter_mine_launcher_deaths: int
    b6_obliterator_kills: int
    b6_obliterator_deaths: int
    scorpion_flail_kills: int
    scorpion_flail_deaths: int
    holoshield_launcher_kills: int
    holoshield_launcher_deaths: int


class DeadlockedCustomGamemodeSchema(BaseModel):
    rank: int
    wins: int
    losses: int
    games_played: int
    time_played: int


class DeadlockedCustomCompetitiveGamemodeSchema(DeadlockedCustomGamemodeSchema):
    kills: int
    deaths: int


class DeadlockedHorizonStatsSchema(BaseModel):
    total_bolts: int
    current_bolts: int


class DeadlockedSNDStatsSchema(DeadlockedCustomCompetitiveGamemodeSchema):
    plants: int
    defuses: int
    ninja_defuses: int
    wins_attacking: int
    wins_defending: int


class DeadlockedPayloadStatsSchema(DeadlockedCustomCompetitiveGamemodeSchema):
    points: int
    kills_while_hot: int
    kills_on_hot: int


class DeadlockedSpleefStatsSchema(DeadlockedCustomGamemodeSchema):
    rounds_played: int
    points: int
    boxes_broken: int


class DeadlockedInfectedStatsSchema(DeadlockedCustomCompetitiveGamemodeSchema):
    infections: int
    times_infected: int
    wins_as_survivor: int
    wins_as_first_infected: int


class DeadlockedGungameStatsSchema(DeadlockedCustomCompetitiveGamemodeSchema):
    promotions: int
    demotions: int
    times_demoted: int


class DeadlockedInfiniteClimberStatsSchema(DeadlockedCustomGamemodeSchema):
    high_score: int


class DeadlockedSurvivalStatsSchema(BaseModel):
    rank: int
    games_played: int
    time_played: int
    kills: int
    deaths: int
    revives: int
    times_revived: int
    mystery_box_rolls: int
    demon_bells_activated: int
    times_activated_power: int
    tokens_used_on_gates: int

    wrench_kills: int
    dual_viper_kills: int
    magma_cannon_kills: int
    arbiter_kills: int
    fusion_rifle_kills: int
    hunter_mine_launcher_kills: int
    b6_obliterator_kills: int
    scorpion_flail_kills: int


class DeadlockedSurvivalMapStatsSchema(BaseModel):
    solo_high_score: int
    coop_high_score: int
    xp: int
    prestige: int


class DeadlockedTrainingStatsSchema(BaseModel):
    rank: int
    games_played: int
    time_played: int
    total_kills: int

    fusion_best_points: int
    fusion_best_time: int
    fusion_kills: int
    fusion_hits: int
    fusion_misses: int
    fusion_accuracy: int
    fusion_best_combo: int

    cycle_best_points: int
    cycle_best_combo: int
    cycle_kills: int
    cycle_deaths: int
    cycle_fusion_hits: int
    cycle_fusion_misses: int
    cycle_fusion_accuracy: int


class DeadlockedPlayerDetailsSchema(BaseModel):

    horizon_id: int
    username: str

    overall_stats: DeadlockedOverallStatsSchema
    deathmatch_stats: DeadlockedDeathmatchStatsSchema
    conquest_stats: DeadlockedConquestStatsSchema
    ctf_stats: DeadlockedCTFStatsSchema
    koth_stats: DeadlockedGameModeWithTimeSchema
    juggernaut_stats: DeadlockedGameModeWithTimeSchema
    weapon_stats: DeadlockedWeaponStatsSchema
    vehicle_stats: DeadlockedVehicleStatsSchema

    horizon_stats: DeadlockedHorizonStatsSchema
    snd_stats: DeadlockedSNDStatsSchema
    payload_stats: DeadlockedPayloadStatsSchema
    spleef_stats: DeadlockedSpleefStatsSchema
    infected_stats: DeadlockedInfectedStatsSchema
    gungame_stats: DeadlockedGungameStatsSchema
    infinite_climber_stats: DeadlockedInfiniteClimberStatsSchema
    survival_stats: DeadlockedSurvivalStatsSchema
    survival_orxon_stats: DeadlockedSurvivalMapStatsSchema
    survival_mountain_pass_stats: DeadlockedSurvivalMapStatsSchema
    survival_veldin_stats: DeadlockedSurvivalMapStatsSchema
    training_stats: DeadlockedTrainingStatsSchema
