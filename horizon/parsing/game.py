from typing import List, Dict
from horizon.parsing.game_rules import GameRules


class Game:

    def __init__(self, game_json: Dict):
        self._id = int(game_json["Id"])
        self._game_id = int(game_json["GameId"])
        self._app_id = int(game_json["AppId"])
        self._min_players = int(game_json["MinPlayers"])
        self._max_players = int(game_json["MaxPlayers"])
        self._starting_players = [int(player_id) for player_id in game_json["PlayerListStart"].split(",")]
        self._game_level = int(game_json["GameLevel"])

        self._game_name = game_json["GameName"]

        self._clan_war = (game_json["GenericField7"] & 0x8000) != 0

        self._rules = GameRules(game_json)

    @property
    def id(self) -> int:
        """
        Horizon Database primary key of the game.
        """
        return self._id

    @property
    def game_id(self) -> int:
        """
        Deadlocked Database primary key of the game.
        """
        return self._game_id

    @property
    def app_id(self) -> int:
        """
        Accessing Application ID. Not applicable for most uses.
        """
        return self._app_id

    @property
    def min_players(self) -> int:
        """
        The minimum number of players allowed. This is a Medius field not applicable to Deadlocked.
        """
        return self._min_players

    @property
    def max_players(self) -> int:
        """
        The maximum number of players allowed. This is a Medius field not applicable to Deadlocked.
        """
        return self._max_players

    @property
    def starting_players(self) -> List[int]:
        """
        List of player IDs for all starting players.
        """
        return self._starting_players[:]

    @property
    def game_level(self) -> int:
        """
        Integer ID of a vanilla map (or the ID of the base map for a custom level).
        """
        return self._game_level

    @property
    def game_name(self) -> str:
        """
        Original name of the lobby/game.
        """
        return self._game_name

    @property
    def clan_war(self) -> bool:
        """
        True if the game was started as a clan war, otherwise False.
        """
        return self._clan_war

    @property
    def rules(self) -> GameRules:
        """
        Game Rules.
        """
        return self._rules
