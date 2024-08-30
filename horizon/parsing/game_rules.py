

class WeaponRules:

    def __init__(self, game_json: dict):
        field: int = game_json["GenericField6"]

        self._dual_vipers: bool = bool(field & 0x00000080)
        self._magma_cannon: bool = bool(field & 0x00000100)
        self._the_arbiter: bool = bool(field & 0x00000200)
        self._fusion_rifle: bool = bool(field & 0x00000400)
        self._hunter_mine_launcher: bool = bool(field & 0x00000800)
        self._b6_obliterator: bool = bool(field & 0x00001000)
        self._holoshield_launcher: bool = bool(field & 0x00002000)
        self._scorpion_flail: bool = bool(field & 0x00040000)

    @property
    def dual_vipers(self) -> bool:
        """
        True if the Dual Vipers are available for the given game, otherwise False.
        """
        return self._dual_vipers

    @property
    def magma_cannon(self) -> bool:
        """
        True if the Magma Cannon is available for the given game, otherwise False.
        """
        return self._magma_cannon

    @property
    def the_arbiter(self) -> bool:
        """
        True if The Arbiter is available for the given game, otherwise False.
        """
        return self._the_arbiter

    @property
    def fusion_rifle(self) -> bool:
        """
        True if the Fusion Rifle is available for the given game, otherwise False.
        """
        return self._the_arbiter

    @property
    def hunter_mine_launcher(self) -> bool:
        """
        True if the Hunter Mine Launcher is available for the given game, otherwise False.
        """
        return self._hunter_mine_launcher

    @property
    def b6_obliterator(self) -> bool:
        """
        True if the B6-Obliterator is available for the given game, otherwise False.
        """
        return self._b6_obliterator

    @property
    def holoshield_launcher(self) -> bool:
        """
        True if the Holoshield Launcher is available for the given game, otherwise False.
        """
        return self._holoshield_launcher

    @property
    def scorpion_flail(self) -> bool:
        """
        True if the Scorpion Flail is available for the given game, otherwise False.
        """
        return self._scorpion_flail


class VehicleRules:

    def __init__(self, game_json: dict):
        field: int = game_json["GenericField6"]

        self._hoverbike: bool = bool(field & 0x00000001)
        self._puma: bool = bool(field & 0x00000002)
        self._hovership: bool = bool(field & 0x00000004)
        self._landstalker: bool = bool(field & 0x00000008)

    @property
    def hoverbike(self) -> bool:
        """
        True if the Hoverbike is available for the given game, otherwise False.
        """
        return self._hoverbike

    @property
    def puma(self) -> bool:
        """
        True if the Puma is available for the given game, otherwise False.
        """
        return self._puma

    @property
    def hovership(self) -> bool:
        """
        True if the Hovership is available for the given game, otherwise False.
        """
        return self._hovership

    @property
    def landstalker(self) -> bool:
        """
        True if the Landstalker is available for the given game, otherwise False.
        """
        return self._landstalker


class GameRules:

    def __init__(self, game_json: dict):

        self._chargeboots: bool = bool(game_json["GenericField6"] & 0x00200000)

        self._weapons: WeaponRules = WeaponRules(game_json)
        self._vehicles: VehicleRules = VehicleRules(game_json)

    @property
    def chargeboots(self) -> bool:
        return self._chargeboots

    @property
    def weapons(self) -> WeaponRules:
        """
        List of weapons rules.
        """
        return self._weapons

    @property
    def vehicles(self) -> WeaponRules:
        """
        List of vehicle rules.
        """
        return self._weapons
