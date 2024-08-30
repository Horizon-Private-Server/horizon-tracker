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

custom_stats_map: dict[int, StatDetails] = {
    0: {"label": "Total Horizon Bolts", "field": "total_horizon_bolts", "table": ""},
    1: {"label": "Current Horizon Bolts", "field": "current_horizon_bolts", "table": ""},

    50: {"label": "SND Rank", "field": "snd_rank", "table": ""},
    51: {"label": "SND Wins", "field": "snd_wins", "table": ""},
    52: {"label": "SND Losses", "field": "snd_losses", "table": ""},
    53: {"label": "SND Games Played", "field": "snd_games_played", "table": ""},
    54: {"label": "SND Kills", "field": "snd_kills", "table": ""},
    55: {"label": "SND Deaths", "field": "snd_deaths", "table": ""},
    56: {"label": "SND Plants", "field": "snd_plants", "table": ""},
    57: {"label": "SND Defuses", "field": "snd_defuses", "table": ""},
    58: {"label": "SND Ninja Defuses", "field": "snd_ninja_defuses", "table": ""},
    59: {"label": "SND Wins Attacking", "field": "snd_wins_attacking", "table": ""},
    60: {"label": "SND Wins Defending", "field": "snd_wins_defending", "table": ""},
    61: {"label": "SND Time Played", "field": "snd_time_played", "table": ""},

    70: {"label": "Payload Rank", "field": "payload_rank", "table": ""},
    71: {"label": "Payload Wins", "field": "payload_wins", "table": ""},
    72: {"label": "Payload Losses", "field": "payload_losses", "table": ""},
    73: {"label": "Payload Games Played", "field": "payload_games_played", "table": ""},
    74: {"label": "Payload Kills", "field": "payload_kills", "table": ""},
    75: {"label": "Payload Deaths", "field": "payload_deaths", "table": ""},
    76: {"label": "Payload Points", "field": "payload_points", "table": ""},
    77: {"label": "Payload Kills While Hot", "field": "payload_kills_while_hot", "table": ""},
    78: {"label": "Payload Kills On Hot", "field": "payload_kills_on_hot", "table": ""},
    79: {"label": "Payload Time Played", "field": "payload_time_played", "table": ""},

    90: {"label": "Spleef Rank", "field": "spleef_rank", "table": ""},
    91: {"label": "Spleef Wins", "field": "spleef_wins", "table": ""},
    92: {"label": "Spleef Losses", "field": "spleef_losses", "table": ""},
    93: {"label": "Spleef Games Played", "field": "spleef_games_played", "table": ""},
    94: {"label": "Spleef Rounds Played", "field": "spleef_rounds_played", "table": ""},
    95: {"label": "Spleef Points", "field": "spleef_points", "table": ""},
    96: {"label": "Spleef Time Played", "field": "spleef_time_played", "table": ""},
    97: {"label": "Spleef Boxes Broken", "field": "spleef_boxes_broken", "table": ""},

    110: {"label": "Infected Rank", "field": "infected_rank", "table": ""},
    111: {"label": "Infected Wins", "field": "infected_wins", "table": ""},
    112: {"label": "Infected Losses", "field": "infected_losses", "table": ""},
    113: {"label": "Infected Games Played", "field": "infected_games_played", "table": ""},
    114: {"label": "Infected Kills", "field": "infected_kills", "table": ""},
    115: {"label": "Infected Deaths", "field": "infected_deaths", "table": ""},
    116: {"label": "Infected Infections", "field": "infected_infections", "table": ""},
    117: {"label": "Infected Times Infected", "field": "infected_times_infected", "table": ""},
    118: {"label": "Infected Time Played", "field": "infected_time_played", "table": ""},
    119: {"label": "Infected Wins As Survivor", "field": "infected_wins_as_survivor", "table": ""},
    120: {"label": "Infected Wins As First Infected", "field": "infected_wins_as_first_infected", "table": ""},

    130: {"label": "Gun Game Rank", "field": "gungame_rank", "table": ""},
    131: {"label": "Gun Game Wins", "field": "gungame_wins", "table": ""},
    132: {"label": "Gun Game Losses", "field": "gungame_losses", "table": ""},
    133: {"label": "Gun Game Games Played", "field": "gungame_games_played", "table": ""},
    134: {"label": "Gun Game Kills", "field": "gungame_kills", "table": ""},
    135: {"label": "Gun Game Deaths", "field": "gungame_deaths", "table": ""},
    136: {"label": "Gun Game Demotions", "field": "gungame_demotions", "table": ""},
    137: {"label": "Gun Game Times Demoted", "field": "gungame_times_demoted", "table": ""},
    138: {"label": "Gun Game Times Promoted", "field": "gungame_times_promoted", "table": ""},
    139: {"label": "Gun Game Time Played", "field": "gungame_time_played", "table": ""},

    150: {"label": "Infinite Climber Rank", "field": "climber_rank", "table": ""},
    151: {"label": "Infinite Climber Wins", "field": "climber_wins", "table": ""},
    152: {"label": "Infinite Climber Losses", "field": "climber_losses", "table": ""},
    153: {"label": "Infinite Climber Games Played", "field": "climber_games_played", "table": ""},
    154: {"label": "Infinite Climber High Score", "field": "climber_high_score", "table": ""},
    155: {"label": "Infinite Climber Time Played", "field": "climber_time_played", "table": ""},

    170: {"label": "Survival Rank", "field": "survival_rank", "table": ""},
    171: {"label": "Survival Games Played", "field": "survival_games_played", "table": ""},
    172: {"label": "Survival Time Played", "field": "survival_time_played", "table": ""},
    173: {"label": "Survival Kills", "field": "survival_kills", "table": ""},
    174: {"label": "Survival Deaths", "field": "survival_deaths", "table": ""},
    175: {"label": "Survival Revives", "field": "survival_revives", "table": ""},
    176: {"label": "Survival Times Revived", "field": "survival_times_revived", "table": ""},

    177: {"label": "Survival Orxon Solo High Score", "field": "survival_map1_solo_high_score", "table": ""},
    178: {"label": "Survival Orxon Coop High Score", "field": "survival_map1_coop_high_score", "table": ""},
    179: {"label": "Survival Mountain Pass Solo High Score", "field": "survival_map2_solo_high_score", "table": ""},
    180: {"label": "Survival Mountain Pass Coop High Score", "field": "survival_map2_coop_high_score", "table": ""},
    181: {"label": "Survival Veldin Solo High Score", "field": "survival_map3_solo_high_score", "table": ""},

    182: {"label": "Survival Wrench Kills", "field": "survival_wrench_kills", "table": ""},
    183: {"label": "Survival Dual Viper Kills", "field": "survival_dual_viper_kills", "table": ""},
    184: {"label": "Survival Magma Cannon Kills", "field": "survival_magma_cannon_kills", "table": ""},
    185: {"label": "Survival Arbiter Kills", "field": "survival_arbiter_kills", "table": ""},
    186: {"label": "Survival Fusion Rifle Kills", "field": "survival_fusion_rifle_kills", "table": ""},
    187: {"label": "Survival Mine Launcher Kills", "field": "survival_mine_launcher_kills", "table": ""},
    188: {"label": "Survival B6 Obliterator Kills", "field": "survival_b6_obliterator_kills", "table": ""},
    189: {"label": "Survival Scorpion Flail Kills", "field": "survival_scorpion_flail_kills", "table": ""},

    190: {"label": "Survival Orxon XP", "field": "survival_map1_xp", "table": ""},

    191: {"label": "Survival Times Rolled Mystery Box", "field": "survival_times_rolled_mystery_box", "table": ""},
    192: {"label": "Survival Times Activated Demon Bell", "field": "survival_times_activated_demon_bell", "table": ""},
    193: {"label": "Survival Times Activated Power", "field": "survival_times_activated_power", "table": ""},
    194: {"label": "Survival Tokens Used On Gates", "field": "survival_tokens_used_on_gates", "table": ""},

    195: {"label": "Survival Veldin Coop High Score", "field": "survival_map3_coop_high_score", "table": ""},
    196: {"label": "Survival Orxon Prestige", "field": "survival_map1_prestige", "table": ""},
    197: {"label": "Survival Mountain Pass XP", "field": "survival_map2_xp", "table": ""},
    198: {"label": "Survival Mountain Pass Prestige", "field": "survival_map2_prestige", "table": ""},
    199: {"label": "Survival Veldin XP", "field": "survival_map3_xp", "table": ""},
    200: {"label": "Survival Veldin Prestige", "field": "survival_map3_prestige", "table": ""},

    210: {"label": "Training Rank", "field": "training_rank", "table": ""},
    211: {"label": "Training Games Played", "field": "training_games_played", "table": ""},
    212: {"label": "Training Time Played", "field": "training_time_played", "table": ""},
    213: {"label": "Training Total Kills", "field": "training_total_kills", "table": ""},
    214: {"label": "Training Fusion Best Points", "field": "training_fusion_best_points", "table": ""},
    215: {"label": "Training Fusion Best Time", "field": "training_fusion_best_time", "table": ""},
    216: {"label": "Training Fusion Kills", "field": "training_fusion_kills", "table": ""},
    217: {"label": "Training Fusion Hits", "field": "training_fusion_hits", "table": ""},
    218: {"label": "Training Fusion Misses", "field": "training_fusion_misses", "table": ""},
    219: {"label": "Training Fusion Accuracy", "field": "training_fusion_accuracy", "table": ""},
    220: {"label": "Training Fusion Best Combo", "field": "training_fusion_best_combo", "table": ""},
    221: {"label": "Training Cycle Best Points", "field": "training_cycle_best_points", "table": ""},
    222: {"label": "Training Cycle Best Combo", "field": "training_cycle_best_combo", "table": ""},
    223: {"label": "Training Cycle Kills", "field": "training_cycle_kills", "table": ""},
    224: {"label": "Training Cycle Deaths", "field": "training_cycle_deaths", "table": ""},
    225: {"label": "Training Cycle Fusion Hits", "field": "training_cycle_fusion_hits", "table": ""},
    226: {"label": "Training Cycle Fusion Misses", "field": "training_cycle_fusion_misses", "table": ""},
    227: {"label": "Training Cycle Fusion Accuracy", "field": "training_cycle_fusion_accuracy", "table": ""},
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
