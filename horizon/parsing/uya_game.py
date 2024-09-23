import struct

MAP_BITMAP = {
    "00001":"Bakisi Isles",
    "00010":"Hoven Gorge",
    "00011":"Outpost x12",
    "00100":"Korgon Outpost",
    "00101":"Metropolis",
    "00110":"Blackwater City",
    "00111":"Command Center",
    "01001":'Aquatos Sewers',
    "01000": "Blackwater Dox",
    "01010":"Marcadia Palace",
}

TIME_BITMAP = {
    '000':'No Time Limit',
    '001':"5 Minutes",
    '010':"10 Minutes",
    '011':"15 Minutes",
    "100":"20 Minutes",
    "101":"25 Minutes",
    "110":"30 Minutes",
    "111":"35 Minutes",
}

MODE_BITMAP = { #3,4
    '00':"Siege",
    '01':"CTF",
    '10':"Deathmatch"
}

SUBMODE_BITMAP = {
    # '1':"no_teams", #13
    # "1":"base_attrition" #20
    'isTeams':13, #1 = yes, means u can swap teams only 0 in DM
    "isAttrition":20, #1 = yes #consitutes also as chaos ctf
}


def try_parse_value(func, num):
    # Internal parsing tool for parsing
    try:
        return func(num)
    except:
        return func(num+2**32)


def uya_map_parser(generic_field_3: int) -> str:
    # Pass in Generic Field 3 (integer)
    def internal_parser(num):
        '''Accepts generic_field_3 INTEGER number (which is 4 a byte long hex string)'''
        num = int(num) if type(num) != 'int' else num
        num = struct.pack('<I', num).hex()
        num=num[0:2]
        num = int(num,16)
        num = format(num, "#010b")[2:]
        game_map = num[:5]
        game_map = MAP_BITMAP[game_map]
        return game_map

    try:
        map = try_parse_value(internal_parser, generic_field_3)
    except:
        map = 'Unknown map!' 

    return map



def uya_time_parser(generic_field_3: int) -> str:
    # Pass in Generic Field 3 (integer)
    def internal_parser(num):

        '''Accepts generic_field_3 INTEGER number (which is 4 a byte long hex string)'''
        num = int(num) if type(num) != 'int' else num
        num = struct.pack('<I', num).hex()
        num=num[0:2]
        num = int(num,16)
        num = format(num, "#010b")[2:]
        game_time = num[5:]
        game_time = TIME_BITMAP[game_time]
        return game_time

    try:
        val = try_parse_value(internal_parser, generic_field_3)
    except:
        val = 'Unknown Time!' 

    return val



def uya_gamemode_parser(generic_field_3: int) -> tuple[str, str]:
    # Pass in Generic Field 3 (integer)

    def internal_parser(num):
        '''Accepts generic_field_3 INTEGER number (which is 4 a byte long hex string)
        returns game MODE andd game SUBMODE/ type'''
        num = int(num) if type(num) != 'int' else num
        num = struct.pack('<I', num).hex()
        num=num[2:] #cut off the front 2 bytes
        num = int(num,16)
        num = format(num, "#026b")[2:]
        game_mode = MODE_BITMAP[num[3:5]] if num[3:5] in MODE_BITMAP else "Unknown Game Mode"
        isTeams = True if num[SUBMODE_BITMAP['isTeams']] == '1' else False
        isAttrition = True if num[SUBMODE_BITMAP['isAttrition']]== '1' else False

        if game_mode == MODE_BITMAP['00']:
            game_type = "Attrition" if isAttrition else "Normal"
        elif game_mode == MODE_BITMAP['01']:
            game_type = "Chaos" if isAttrition else "Normal"
        elif game_mode == MODE_BITMAP['10']:
            game_type = "Teams" if isTeams else "FFA"
        else:
            game_type = "Game Type Not Found"
        return game_mode, game_type
    try:
        game_mode, game_type = try_parse_value(internal_parser, generic_field_3)
    except:
        game_mode, game_type = 'Unkown Game Mode', 'Unknown Game Type'

    return game_mode, game_type
