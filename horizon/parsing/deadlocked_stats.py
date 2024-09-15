import math
from typing import TypedDict


class StatDetails(TypedDict):
    label: str
    field: str
    table: str


vanilla_stats_map: dict[int, StatDetails] = {
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
    37: {"label": "Hill Time", "field": "time", "table": "koth_stats"},
    38: {"label": "Juggernaut Rank", "field": "rank", "table": "juggernaut_stats"},
    39: {"label": "Juggernaut Wins", "field": "wins", "table": "juggernaut_stats"},
    40: {"label": "Juggernaut Losses", "field": "losses", "table": "juggernaut_stats"},
    41: {"label": "", "field": "", "table": ""},
    42: {"label": "Juggernaut Kills", "field": "kills", "table": "juggernaut_stats"},
    43: {"label": "Juggernaut Deaths", "field": "deaths", "table": "juggernaut_stats"},
    44: {"label": "Juggernaut Time", "field": "time", "table": "juggernaut_stats"},
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

custom_stats_map: dict[int, StatDetails] = {
    0: {"label": "Total Horizon Bolts", "field": "total_bolts", "table": "horizon_stats"},
    1: {"label": "Current Horizon Bolts", "field": "current_bolts", "table": "horizon_stats"},

    50: {"label": "SND Rank", "field": "rank", "table": "snd_stats"},
    51: {"label": "SND Wins", "field": "wins", "table": "snd_stats"},
    52: {"label": "SND Losses", "field": "losses", "table": ""},
    53: {"label": "SND Games Played", "field": "games_played", "table": "snd_stats"},
    54: {"label": "SND Kills", "field": "kills", "table": "snd_stats"},
    55: {"label": "SND Deaths", "field": "deaths", "table": "snd_stats"},
    56: {"label": "SND Plants", "field": "plants", "table": "snd_stats"},
    57: {"label": "SND Defuses", "field": "defuses", "table": "snd_stats"},
    58: {"label": "SND Ninja Defuses", "field": "ninja_defuses", "table": "snd_stats"},
    59: {"label": "SND Wins Attacking", "field": "wins_attacking", "table": "snd_stats"},
    60: {"label": "SND Wins Defending", "field": "wins_defending", "table": "snd_stats"},
    61: {"label": "SND Time Played", "field": "time_played", "table": "snd_stats"},

    70: {"label": "Payload Rank", "field": "rank", "table": "payload_stats"},
    71: {"label": "Payload Wins", "field": "wins", "table": "payload_stats"},
    72: {"label": "Payload Losses", "field": "losses", "table": "payload_stats"},
    73: {"label": "Payload Games Played", "field": "games_played", "table": "payload_stats"},
    74: {"label": "Payload Kills", "field": "kills", "table": "payload_stats"},
    75: {"label": "Payload Deaths", "field": "deaths", "table": "payload_stats"},
    76: {"label": "Payload Points", "field": "points", "table": "payload_stats"},
    77: {"label": "Payload Kills While Hot", "field": "kills_while_hot", "table": "payload_stats"},
    78: {"label": "Payload Kills On Hot", "field": "kills_on_hot", "table": "payload_stats"},
    79: {"label": "Payload Time Played", "field": "time_played", "table": "payload_stats"},

    90: {"label": "Spleef Rank", "field": "rank", "table": "spleef_stats"},
    91: {"label": "Spleef Wins", "field": "wins", "table": "spleef_stats"},
    92: {"label": "Spleef Losses", "field": "losses", "table": "spleef_stats"},
    93: {"label": "Spleef Games Played", "field": "games_played", "table": "spleef_stats"},
    94: {"label": "Spleef Rounds Played", "field": "rounds_played", "table": "spleef_stats"},
    95: {"label": "Spleef Points", "field": "points", "table": "spleef_stats"},
    96: {"label": "Spleef Time Played", "field": "time_played", "table": "spleef_stats"},
    97: {"label": "Spleef Boxes Broken", "field": "boxes_broken", "table": "spleef_stats"},

    110: {"label": "Infected Rank", "field": "rank", "table": "infected_stats"},
    111: {"label": "Infected Wins", "field": "wins", "table": "infected_stats"},
    112: {"label": "Infected Losses", "field": "losses", "table": "infected_stats"},
    113: {"label": "Infected Games Played", "field": "games_played", "table": "infected_stats"},
    114: {"label": "Infected Kills", "field": "kills", "table": "infected_stats"},
    115: {"label": "Infected Deaths", "field": "deaths", "table": "infected_stats"},
    116: {"label": "Infected Infections", "field": "infections", "table": "infected_stats"},
    117: {"label": "Infected Times Infected", "field": "times_infected", "table": "infected_stats"},
    118: {"label": "Infected Time Played", "field": "time_played", "table": "infected_stats"},
    119: {"label": "Infected Wins As Survivor", "field": "wins_as_survivor", "table": "infected_stats"},
    120: {"label": "Infected Wins As First Infected", "field": "wins_as_first_infected", "table": "infected_stats"},

    130: {"label": "Gun Game Rank", "field": "rank", "table": "gungame_stats"},
    131: {"label": "Gun Game Wins", "field": "wins", "table": "gungame_stats"},
    132: {"label": "Gun Game Losses", "field": "losses", "table": "gungame_stats"},
    133: {"label": "Gun Game Games Played", "field": "games_played", "table": "gungame_stats"},
    134: {"label": "Gun Game Kills", "field": "kills", "table": "gungame_stats"},
    135: {"label": "Gun Game Deaths", "field": "deaths", "table": "gungame_stats"},
    136: {"label": "Gun Game Demotions", "field": "demotions", "table": "gungame_stats"},
    137: {"label": "Gun Game Times Demoted", "field": "times_demoted", "table": "gungame_stats"},
    138: {"label": "Gun Game Times Promoted", "field": "promotions", "table": "gungame_stats"},
    139: {"label": "Gun Game Time Played", "field": "time_played", "table": "gungame_stats"},

    150: {"label": "Infinite Climber Rank", "field": "rank", "table": "infinite_climber_stats"},
    151: {"label": "Infinite Climber Wins", "field": "wins", "table": "infinite_climber_stats"},
    152: {"label": "Infinite Climber Losses", "field": "losses", "table": "infinite_climber_stats"},
    153: {"label": "Infinite Climber Games Played", "field": "games_played", "table": "infinite_climber_stats"},
    154: {"label": "Infinite Climber High Score", "field": "high_score", "table": "infinite_climber_stats"},
    155: {"label": "Infinite Climber Time Played", "field": "time_played", "table": "infinite_climber_stats"},

    170: {"label": "Survival Rank", "field": "rank", "table": "survival_stats"},
    171: {"label": "Survival Games Played", "field": "games_played", "table": "survival_stats"},
    172: {"label": "Survival Time Played", "field": "time_played", "table": "survival_stats"},
    173: {"label": "Survival Kills", "field": "kills", "table": "survival_stats"},
    174: {"label": "Survival Deaths", "field": "deaths", "table": "survival_stats"},
    175: {"label": "Survival Revives", "field": "revives", "table": "survival_stats"},
    176: {"label": "Survival Times Revived", "field": "times_revived", "table": "survival_stats"},

    177: {"label": "Survival Orxon Solo High Score", "field": "solo_high_score", "table": "survival_orxon_stats"},
    178: {"label": "Survival Orxon Coop High Score", "field": "coop_high_score", "table": "survival_orxon_stats"},
    179: {"label": "Survival Mountain Pass Solo High Score", "field": "solo_high_score", "table": "survival_mountain_pass_stats"},
    180: {"label": "Survival Mountain Pass Coop High Score", "field": "coop_high_score", "table": "survival_mountain_pass_stats"},
    181: {"label": "Survival Veldin Solo High Score", "field": "solo_high_score", "table": "survival_veldin_stats"},

    182: {"label": "Survival Wrench Kills", "field": "wrench_kills", "table": "survival_stats"},
    183: {"label": "Survival Dual Viper Kills", "field": "dual_viper_kills", "table": "survival_stats"},
    184: {"label": "Survival Magma Cannon Kills", "field": "magma_cannon_kills", "table": "survival_stats"},
    185: {"label": "Survival Arbiter Kills", "field": "arbiter_kills", "table": "survival_stats"},
    186: {"label": "Survival Fusion Rifle Kills", "field": "fusion_rifle_kills", "table": "survival_stats"},
    187: {"label": "Survival Mine Launcher Kills", "field": "hunter_mine_launcher_kills", "table": "survival_stats"},
    188: {"label": "Survival B6 Obliterator Kills", "field": "b6_obliterator_kills", "table": "survival_stats"},
    189: {"label": "Survival Scorpion Flail Kills", "field": "scorpion_flail_kills", "table": "survival_stats"},

    190: {"label": "Survival Orxon XP", "field": "xp", "table": "survival_orxon_stats"},

    191: {"label": "Survival Times Rolled Mystery Box", "field": "mystery_box_rolls", "table": "survival_stats"},
    192: {"label": "Survival Times Activated Demon Bell", "field": "demon_bells_activated", "table": "survival_stats"},
    193: {"label": "Survival Times Activated Power", "field": "times_activated_power", "table": "survival_stats"},
    194: {"label": "Survival Tokens Used On Gates", "field": "tokens_used_on_gates", "table": "survival_stats"},

    195: {"label": "Survival Veldin Coop High Score", "field": "coop_high_score", "table": "survival_veldin_stats"},
    196: {"label": "Survival Orxon Prestige", "field": "prestige", "table": "survival_orxon_stats"},
    197: {"label": "Survival Mountain Pass XP", "field": "xp", "table": "survival_mountain_pass_stats"},
    198: {"label": "Survival Mountain Pass Prestige", "field": "prestige", "table": "survival_mountain_pass_stats"},
    199: {"label": "Survival Veldin XP", "field": "xp", "table": "survival_veldin_stats"},
    200: {"label": "Survival Veldin Prestige", "field": "prestige", "table": "survival_veldin_stats"},

    210: {"label": "Training Rank", "field": "rank", "table": "training_stats"},
    211: {"label": "Training Games Played", "field": "games_played", "table": "training_stats"},
    212: {"label": "Training Time Played", "field": "time_played", "table": "training_stats"},
    213: {"label": "Training Total Kills", "field": "total_kills", "table": "training_stats"},

    214: {"label": "Training Fusion Best Points", "field": "fusion_best_points", "table": "training_stats"},
    215: {"label": "Training Fusion Best Time", "field": "fusion_best_time", "table": "training_stats"},
    216: {"label": "Training Fusion Kills", "field": "fusion_kills", "table": "training_stats"},
    217: {"label": "Training Fusion Hits", "field": "fusion_hits", "table": "training_stats"},
    218: {"label": "Training Fusion Misses", "field": "fusion_misses", "table": "training_stats"},
    219: {"label": "Training Fusion Accuracy", "field": "fusion_accuracy", "table": "training_stats"},
    220: {"label": "Training Fusion Best Combo", "field": "fusion_best_combo", "table": "training_stats"},

    221: {"label": "Training Cycle Best Points", "field": "cycle_best_points", "table": "training_stats"},
    222: {"label": "Training Cycle Best Combo", "field": "cycle_best_combo", "table": "training_stats"},
    223: {"label": "Training Cycle Kills", "field": "cycle_kills", "table": "training_stats"},
    224: {"label": "Training Cycle Deaths", "field": "cycle_deaths", "table": "training_stats"},
    225: {"label": "Training Cycle Fusion Hits", "field": "cycle_fusion_hits", "table": "training_stats"},
    226: {"label": "Training Cycle Fusion Misses", "field": "cycle_fusion_misses", "table": "training_stats"},
    227: {"label": "Training Cycle Fusion Accuracy", "field": "cycle_fusion_accuracy", "table": "training_stats"},
}


def convert_rank_to_skill_level(rank: int) -> str:
    """
    Converts the numerical Deadlocked Rank into the common skill level number.

    :param rank: Integer rank of a user.
    :return: The corresponding skill level of the player.
    """
    skill_level_table = [0, 200, 800, 1600, 2500, 3500, 5000, 6500, 8000, 9500]

    if rank >= skill_level_table[9]:
        return "10.00"
    if rank <= skill_level_table[0]:
        return "1.00"

    i = 0
    while rank > skill_level_table[i]:
        i += 1

    raw_skill_level: float = i + ((rank - skill_level_table[i - 1]) / (skill_level_table[i] - skill_level_table[i - 1]))
    processed_skill_level: float = math.floor(raw_skill_level * 100) / 100

    return f"{processed_skill_level:.2f}"
