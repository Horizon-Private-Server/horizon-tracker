import math
from itertools import permutations
from typing import Dict, List, Collection, Any, Tuple

DEFAULT = 400
K = 100


def win_rating(winner: int, loser: int, k=K):
    expected, _ = probabilities(winner, loser)
    actual = 1.0
    return winner + (k * (actual - expected))


def loss_rating(winner: int, loser: int, k=K):
    expected, _ = probabilities(winner, loser)
    actual = 0.0
    result = winner + (k * (actual - expected))
    return result if result > 0 else 0


def probability(_r1: int, _r2: int) -> float:
    return 1.0 / (1.0 + pow(10, ((_r1 - _r2) / DEFAULT)))


def probabilities(rating1: int, rating2: int) -> (float, float):
    return probability(rating1, rating2), probability(rating2, rating1)


def compute_elo(players: List[Dict]) -> List[Dict]:

    sorted_players = list(sorted(players, key=lambda _player: _player["score"], reverse=True))

    if len(sorted_players) % 2 == 1:
        winners = sorted_players[0:int(len(sorted_players) / 2) - 1]
        losers = sorted_players[int(len(sorted_players) / 2):len(sorted_players)]
    else:
        winners = sorted_players[0:int(len(sorted_players) / 2)]
        losers = sorted_players[int(len(sorted_players) / 2):len(sorted_players)]

    winners_avg_elo = sum([winner["rank"] for winner in winners]) / len(winners)
    losers_avg_elo = sum([loser["rank"] for loser in losers]) / len(losers)

    winners_avg_updated_elo = round(win_rating(winners_avg_elo, losers_avg_elo))
    losers_avg_updated_elo = round(loss_rating(losers_avg_elo, winners_avg_elo))

    winners_delta_avg_elo = winners_avg_updated_elo - winners_avg_elo
    losers_delta_avg_elo = losers_avg_updated_elo - losers_avg_elo

    winners_spoils = math.ceil(winners_delta_avg_elo / len(winners))
    losers_losses = math.ceil(losers_delta_avg_elo / len(losers))

    for winner in winners:
        winner["rank"] = round(winner["rank"] + winners_spoils)

    for loser in losers:
        loser["rank"] = round(loser["rank"] + losers_losses)

    return winners + losers


def generate_teams(players: Collection[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], ...]:
    """
    Generates 2 even teams based on the average Elo rating of players in the source group.

    :param players: A Collection of players ({"rank": <float|int>, ...}) with an Elo score ("rank").
    :return: Two teams based on the input collection returned as a Tuple.
    """

    assert len(players) % 2 == 0, "Teams must be even."

    combination_lookup: Dict[float, Any] = dict()
    lowest: float = float("inf")

    for combination in permutations(players, len(players)):
        team1: Collection[Dict[str, Any]] = combination[0:int(len(combination)/2)]
        team2: Collection[Dict[str, Any]] = combination[int(len(combination)/2):len(combination)]
        avg_elo1: float = sum([p["rank"] for p in team1]) / len(team1)
        avg_elo2: float = sum([p["rank"] for p in team2]) / len(team2)

        if round(avg_elo1) == round(avg_elo2):
            return list(team1), list(team2)

        _delta: float = math.fabs(avg_elo1 - avg_elo2)

        if _delta < lowest:
            lowest = _delta

        combination_lookup[_delta] = (team1, team2)

    return combination_lookup[lowest]
