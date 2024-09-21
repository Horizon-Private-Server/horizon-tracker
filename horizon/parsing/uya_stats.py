import math
from typing import TypedDict


class StatDetails(TypedDict):
    label: str
    field: str
    table: str


uya_vanilla_stats_map: dict[int, StatDetails] = {
    0: {'label': '', 'field': '', 'table': ''},
    1: {'label': 'Overall Rank', 'field': 'rank', 'table': 'overall_stats'},
    2: {'label': 'Wins', 'field': 'wins', 'table': 'overall_stats'},
    3: {'label': 'Losses', 'field': 'losses', 'table': 'overall_stats'},
    4: {'label': 'Win-Loss Ratio', 'field': 'wl_ratio', 'table': 'overall_stats'},
    5: {'label': 'Kills', 'field': 'kills', 'table': 'overall_stats'},
    6: {'label': 'Deaths', 'field': 'deaths', 'table': 'overall_stats'},
    7: {'label': 'Suicides', 'field': 'suicides', 'table': 'overall_stats'},
    8: {'label': 'Kill-Death Ratio', 'field': 'kd_ratio', 'table': 'overall_stats'},
    9: {'label': 'Total Base Damage', 'field': 'base_dmg', 'table': 'overall_stats'},
    10: {'label': 'Total Nodes', 'field': 'nodes', 'table': 'overall_stats'},
    11: {'label': 'Total Games Played', 'field': 'games_played', 'table': 'overall_stats'},
    12: {'label': '', 'field': '', 'table': ''},
    13: {'label': '', 'field': '', 'table': ''},
    14: {'label': '', 'field': '', 'table': ''},
    15: {'label': '', 'field': '', 'table': ''},
    16: {'label': 'Deathmatch Rank', 'field': 'rank', 'table': 'deathmatch_stats'},
    17: {'label': 'Siege Rank', 'field': 'rank', 'table': 'siege_stats'},
    18: {'label': 'CTF Rank', 'field': 'rank', 'table': 'ctf_stats'},
    19: {'label': '', 'field': '', 'table': ''},
    20: {'label': 'N60 Deaths', 'field': 'n60_deaths', 'table': 'weapon_stats'},
    21: {'label': 'N60 Kills', 'field': 'n60_kills', 'table': 'weapon_stats'},
    22: {'label': 'Lava Gun Deaths', 'field': 'lava_gun_deaths', 'table': 'weapon_stats'},
    23: {'label': 'Lava Gun Kills', 'field': 'lava_gun_kills', 'table': 'weapon_stats'},
    24: {'label': 'Gravity Bomb Deaths', 'field': 'gravity_bomb_deaths', 'table': 'weapon_stats'},
    25: {'label': 'Gravity Bomb Kills', 'field': 'gravity_bomb_kills', 'table': 'weapon_stats'},
    26: {'label': 'Flux Rifle Deaths', 'field': 'flux_rifle_deaths', 'table': 'weapon_stats'},
    27: {'label': 'Flux Rifle Kills', 'field': 'flux_rifle_kills', 'table': 'weapon_stats'},
    28: {'label': 'Mins Glove Deaths', 'field': 'mine_glove_deaths', 'table': 'weapon_stats'},
    29: {'label': 'Mine Glove Kills', 'field': 'min_glove_kills', 'table': 'weapon_stats'},
    30: {'label': 'Morph-O-Ray Deaths', 'field': 'morph_deaths', 'table': 'weapon_stats'},
    31: {'label': 'Morph-O-Ray Kills', 'field': 'morph_kills', 'table': 'weapon_stats'},
    32: {'label': 'Blitz Cannon Deaths', 'field': 'blitz_deaths', 'table': 'weapon_stats'},
    33: {'label': 'Blitz Cannon Kills', 'field': 'blitz_kills', 'table': 'weapon_stats'},
    34: {'label': 'Rocket Deaths', 'field': 'rocket_deaths', 'table': 'weapon_stats'},
    35: {'label': 'Rocket Kills', 'field': 'rocket_kills', 'table': 'weapon_stats'},
    36: {'label': 'Wrench Deaths', 'field': 'wrench_deaths', 'table': 'weapon_stats'},
    37: {'label': 'Wrench Kills', 'field': 'wrench_kills', 'table': 'weapon_stats'},
    38: {'label': 'Siege Wins', 'field': 'wins', 'table': 'siege_stats'},
    39: {'label': 'Siege Losses', 'field': 'losses', 'table': 'siege_stats'},
    40: {'label': 'Siege Win-Loss Ratio', 'field': 'wl_ratio', 'table': 'siege_stats'},
    41: {'label': 'Siege Kills', 'field': 'kills', 'table': 'siege_stats'},
    42: {'label': 'Siege Deaths', 'field': 'deaths', 'table': 'siege_stats'},
    43: {'label': 'Siege Kill-Death Ratio', 'field': 'kd_ratio', 'table': 'siege_stats'},
    44: {'label': 'Siege Base Damage', 'field': 'base_dmg', 'table': 'siege_stats'},
    45: {'label': 'Siege Nodes', 'field': 'nodes', 'table': 'siege_stats'},
    46: {'label': 'Siege Games Played', 'field': 'games_played', 'table': 'siege_stats'},
    47: {'label': 'Deathmatch Wins', 'field': 'wins', 'table': 'deathmatch_stats'},
    48: {'label': 'Deathmatch Losses', 'field': 'losses', 'table': 'deathmatch_stats'},
    49: {'label': 'Deathmatch Win-Loss Ratio', 'field': 'wl_ratio', 'table': 'deathmatch_stats'},
    50: {'label': 'Deathmatch Kills', 'field': 'kills', 'table': 'deathmatch_stats'},
    51: {'label': 'Deathmatch Deaths', 'field': 'deaths', 'table': 'deathmatch_stats'},
    52: {'label': 'Deathmatch Kill-Death Ratio', 'field': 'kd_ratio', 'table': 'deathmatch_stats'},
    53: {'label': 'Deathmatch Games Played', 'field': 'games_played', 'table': 'deathmatch_stats'},
    54: {'label': 'CTF Wins', 'field': 'wins', 'table': 'ctf_stats'},
    55: {'label': 'CTF Losses', 'field': 'losses', 'table': 'ctf_stats'},
    56: {'label': 'CTF W/L Ratio', 'field': 'wl_ratio', 'table': 'ctf_stats'},
    57: {'label': 'CTF Kills', 'field': 'kills', 'table': 'ctf_stats'},
    58: {'label': 'CTF Deaths', 'field': 'deaths', 'table': 'ctf_stats'},
    59: {'label': 'CTF K/D Ratio', 'field': 'kd_ratio', 'table': 'ctf_stats'},
    60: {'label': 'CTF Base Damage', 'field': 'base_dmg', 'table': 'ctf_stats'},
    61: {'label': 'CTF Nodes', 'field': 'nodes', 'table': 'ctf_stats'},
    62: {'label': 'CTF Flags Captured', 'field': 'flag_captures', 'table': 'ctf_stats'},
    63: {'label': 'CTF Flags Saved', 'field': 'flag_saves', 'table': 'ctf_stats'},
    64: {'label': 'CTF Games Played', 'field': 'games_played', 'table': 'ctf_stats'},
    65: {'label': '', 'field': '', 'table': ''},
    66: {'label': 'Siege Suicides', 'field': 'suicides', 'table': 'siege_stats'},
    67: {'label': 'CTF Suicides', 'field': 'suicides', 'table': 'ctf_stats'},
    68: {'label': 'Deathmatch Suicides', 'field': 'suicides', 'table': 'deathmatch_stats'},
    69: {'label': 'Average Kills', 'field': 'avg_kills', 'table': 'overall_stats'},
    70: {'label': 'Average Deaths', 'field': 'avg_deaths', 'table': 'overall_stats'},
    71: {'label': 'Average Suicides', 'field': 'avg_suicides', 'table': 'overall_stats'},
    72: {'label': 'Average Nodes', 'field': 'avg_nodes', 'table': 'overall_stats'},
    73: {'label': 'Average Base Damage', 'field': 'avg_base_dmg', 'table': 'overall_stats'},
    74: {'label': 'Siege Average Kills', 'field': 'avg_kills', 'table': 'siege_stats'},
    75: {'label': 'Siege Average Deaths', 'field': 'avg_deaths', 'table': 'siege_stats'},
    76: {'label': 'Siege Average Nodes', 'field': 'avg_nodes', 'table': 'siege_stats'},
    77: {'label': 'Siege Average Base Damage', 'field': 'avg_base_dmg', 'table': 'siege_stats'},
    78: {'label': 'Siege Average Suicides', 'field': 'avg_suicides', 'table': 'siege_stats'},
    79: {'label': 'CTF Average Kills', 'field': 'avg_kills', 'table': 'ctf_stats'},
    80: {'label': 'CTF Average Deaths', 'field': 'avg_deaths', 'table': 'ctf_stats'},
    81: {'label': 'CTF Average Nodes', 'field': 'avg_nodes', 'table': 'ctf_stats'},
    82: {'label': 'CTF Average Base Damage', 'field': 'avg_base_dmg', 'table': 'ctf_stats'},
    83: {'label': 'CTF Average Flags', 'field': 'avg_flag_captures', 'table': 'ctf_stats'},
    84: {'label': 'CTF Average Flag Saves', 'field': 'avg_flag_saves', 'table': 'ctf_stats'},
    85: {'label': 'CTF Average Suicides', 'field': 'avg_suicides', 'table': 'ctf_stats'},
    86: {'label': 'Deathmatch Average Kills', 'field': 'avg_kills', 'table': 'deathmatch_stats'},
    87: {'label': 'Deathmatch Average Deaths', 'field': 'avg_deaths', 'table': 'deathmatch_stats'},
    88: {'label': 'Deathmatch Average Suicides', 'field': 'avg_suicides', 'table': 'deathmatch_stats'},
    89: {'label': 'Total Squats', 'field': 'squats', 'table': 'overall_stats'},
    90: {'label': 'Average Squats', 'field': 'avg_squats', 'table': 'overall_stats'},
    91: {'label': 'Squat-Kill Ratio', 'field': 'sq_ratio', 'table': 'overall_stats'},
    92: {'label': 'Total Times Squatted', 'field': 'total_times_squatted', 'table': 'overall_stats'},
    93: {'label': 'Average Times Squatted On', 'field': 'avg_squatted_on', 'table': 'overall_stats'},
    94: {'label': 'Squatted/Death Ratio', 'field': 'sd_ratio', 'table': 'overall_stats'},
    95: {'label': 'Total Team Squats', 'field': 'total_team_squats', 'table': 'overall_stats'},
    96: {'label': 'Average Team Squats', 'field': 'avg_team_squats', 'table': 'overall_stats'},
    97: {'label': '', 'field': '', 'table': ''},
    98: {'label': '', 'field': '', 'table': ''},
    99: {'label': '', 'field': '', 'table': ''},
}
