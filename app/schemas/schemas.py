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
