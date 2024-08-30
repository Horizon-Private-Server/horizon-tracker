import math

vanilla_stats_map: dict[int, dict[str, str]] = {
    0: {"label": "", "field": "", "table": ""},
    1: {"label": "", "field": "", "table": ""},
    2: {"label": "Overall Rank", "field": "rank", "table": "overall_stats"},
    3: {"label": "Wins", "field": "wins", "table": "overall_stats"},
    4: {"label": "Losses", "field": "losses", "table": "overall_stats"},
    5: {"label": "Disconnects", "field": "disconnects", "table": "overall_stats"},
    6: {"label": "Kills", "field": "kills", "table": "overall_stats"},
    7: {"label": "Deaths", "field": "deaths", "table": "overall_stats"},
    8: {"label": "Games Played", "field": "games_played", "table": "overall_stats"},
    9: {"label": "", "field": "", "table": ""},
    10: {"label": "", "field": "", "table": ""},
    11: {"label": "Deathmatch Rank", "field": "rank", "table": "deathmatch_stats"},
    12: {"label": "Deathmatch Wins", "field": "wins", "table": "deathmatch_stats"},
    13: {"label": "Deathmatch Losses", "field": "losses", "table": "deathmatch_stats"},
    14: {"label": "", "field": "", "table": ""},
    15: {"label": "Deathmatch Kills", "field": "kills", "table": "deathmatch_stats"},
    16: {"label": "Deathmatch Deaths", "field": "deaths", "table": "deathmatch_stats"},
    17: {"label": "Conquest Rank", "field": "rank", "table": "conquest_stats"},
    18: {"label": "Conquest Wins", "field": "wins", "table": "conquest_stats"},
    19: {"label": "Conquest Losses", "field": "losses", "table": "conquest_stats"},
    20: {"label": "", "field": "", "table": ""},
    21: {"label": "Conquest Kills", "field": "kills", "table": "conquest_stats"},
    22: {"label": "Conquest Deaths", "field": "deaths", "table": "conquest_stats"},
    23: {"label": "Conquest Nodes Taken", "field": "nodes_taken", "table": "conquest_stats"},
    24: {"label": "CTF Rank", "field": "rank", "table": "ctf_stats"},
    25: {"label": "CTF Wins", "field": "wins", "table": "ctf_stats"},
    26: {"label": "CTF Losses", "field": "losses", "table": "ctf_stats"},
    27: {"label": "", "field": "", "table": ""},
    28: {"label": "CTF Kills", "field": "kills", "table": "ctf_stats"},
    29: {"label": "CTF Deaths", "field": "deaths", "table": "ctf_stats"},
    30: {"label": "CTF Flags Captured", "field": "flags_captured", "table": "ctf_stats"},
    31: {"label": "KOTH Rank", "field": "rank", "table": "koth_stats"},
    32: {"label": "KOTH Wins", "field": "wins", "table": "koth_stats"},
    33: {"label": "KOTH Losses", "field": "losses", "table": "koth_stats"},
    34: {"label": "", "field": "", "table": ""},
    35: {"label": "KOTH Kills", "field": "kills", "table": "koth_stats"},
    36: {"label": "KOTH Deaths", "field": "deaths", "table": "koth_stats"},
    37: {"label": "Hill Time", "field": "hill_time", "table": "koth_stats"},
    38: {"label": "Juggernaut Rank", "field": "rank", "table": "juggernaut_stats"},
    39: {"label": "Juggernaut Wins", "field": "wins", "table": "juggernaut_stats"},
    40: {"label": "Juggernaut Losses", "field": "losses", "table": "juggernaut_stats"},
    41: {"label": "", "field": "", "table": ""},
    42: {"label": "Juggernaut Kills", "field": "kills", "table": "juggernaut_stats"},
    43: {"label": "Juggernaut Deaths", "field": "deaths", "table": "juggernaut_stats"},
    44: {"label": "Juggernaut Time", "field": "juggernaut_time", "table": "juggernaut_stats"},
    45: {"label": "Wrench Kills", "field": "wrench_kills", "table": "weapon_stats"},
    46: {"label": "Wrench Deaths", "field": "wrench_deaths", "table": "weapon_stats"},
    47: {"label": "", "field": "", "table": ""},
    48: {"label": "Dual Viper Kills", "field": "dual_viper_kills", "table": "weapon_stats"},
    49: {"label": "Dual Viper Deaths", "field": "dual_viper_deaths", "table": "weapon_stats"},
    50: {"label": "", "field": "", "table": ""},
    51: {"label": "Magma Cannon Kills", "field": "magma_cannon_kills", "table": "weapon_stats"},
    52: {"label": "Magma Cannon Deaths", "field": "magma_cannon_deaths", "table": "weapon_stats"},
    53: {"label": "", "field": "", "table": ""},
    54: {"label": "The Arbiter Kills", "field": "arbiter_kills", "table": "weapon_stats"},
    55: {"label": "The Arbiter Deaths", "field": "arbiter_deaths", "table": "weapon_stats"},
    56: {"label": "", "field": "", "table": ""},
    57: {"label": "Fusion Rifle Kills", "field": "fusion_rifle_kills", "table": "weapon_stats"},
    58: {"label": "Fusion Rifle Deaths", "field": "fusion_rifle_deaths", "table": "weapon_stats"},
    59: {"label": "", "field": "", "table": ""},
    60: {"label": "Hunter Mine Launcher Kills", "field": "hunter_mine_launcher_kills", "table": "weapon_stats"},
    61: {"label": "Hunter Mine Launcher Deaths", "field": "hunter_mine_launcher_deaths", "table": "weapon_stats"},
    62: {"label": "", "field": "", "table": ""},
    63: {"label": "B6-Obliterator Kills", "field": "b6_obliterator_kills", "table": "weapon_stats"},
    64: {"label": "B6-Obliterator Deaths", "field": "b6_obliterator_deaths", "table": "weapon_stats"},
    65: {"label": "", "field": "", "table": ""},
    66: {"label": "Scorpion Flail Kills", "field": "scorpion_flail_kills", "table": "weapon_stats"},
    67: {"label": "Scorpion Flail Deaths", "field": "scorpion_flail_deaths", "table": "weapon_stats"},
    68: {"label": "", "field": "", "table": ""},
    69: {"label": "", "field": "", "table": ""},
    70: {"label": "Roadkills", "field": "roadkills", "table": "vehicle_stats"},
    71: {"label": "Vehicle Squats", "field": "squats", "table": "vehicle_stats"},
    72: {"label": "Squats", "field": "squats", "table": "overall_stats"},
    73: {"label": "Holoshield Launcher Kills", "field": "holoshield_launcher_kills", "table": "weapon_stats"},
    74: {"label": "Holoshield Launcher Deaths", "field": "holoshield_launcher_deaths", "table": "weapon_stats"},
    75: {"label": "", "field": "", "table": ""},
    76: {"label": "", "field": "", "table": ""},
    77: {"label": "", "field": "", "table": ""},
    78: {"label": "", "field": "", "table": ""},
    79: {"label": "", "field": "", "table": ""},
    80: {"label": "", "field": "", "table": ""},
    81: {"label": "", "field": "", "table": ""},
    82: {"label": "", "field": "", "table": ""},
    83: {"label": "", "field": "", "table": ""},
    84: {"label": "", "field": "", "table": ""},
    85: {"label": "", "field": "", "table": ""},
    86: {"label": "", "field": "", "table": ""},
    87: {"label": "", "field": "", "table": ""},
    88: {"label": "", "field": "", "table": ""},
    89: {"label": "", "field": "", "table": ""},
    90: {"label": "", "field": "", "table": ""},
    91: {"label": "", "field": "", "table": ""},
    92: {"label": "", "field": "", "table": ""},
    93: {"label": "", "field": "", "table": ""},
    94: {"label": "", "field": "", "table": ""},
    95: {"label": "", "field": "", "table": ""},
    96: {"label": "", "field": "", "table": ""},
    97: {"label": "", "field": "", "table": ""},
    98: {"label": "", "field": "", "table": ""},
    99: {"label": "", "field": "", "table": ""}
}


def convert_rank_to_skill_level(rank: int) -> float:
    """
    Converts the numerical Deadlocked Rank into the common skill level number.

    :param rank: Integer rank of a user.
    :return: The corresponding skill level of the player.
    """

    skill_level_table = [0, 200, 800, 1600, 2500, 3500, 5000, 6500, 8000, 9500]

    if rank >= skill_level_table[9]:
        return 10.00
    if rank <= skill_level_table[0]:
        return 1.00

    i = 0
    while rank > skill_level_table[i]:
        i += 1

    return math.floor((i + ((rank - skill_level_table[i - 1]) / (skill_level_table[i] - skill_level_table[i - 1]))) * 100) / 100
