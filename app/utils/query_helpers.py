from typing import Union, List, Optional

from sqlalchemy.orm import Session

from app.models.dl import DeadlockedPlayer
from horizon.parsing.deadlocked_stats import vanilla_stats_map


def update_deadlocked_player_vanilla_stats(
    session: Session,
    player_id: Union[int, str],
    player_name: str,
    wide_stats: List[int]
) -> None:

    assert len(wide_stats) == 100, "The provided wide stats length is not 100, please validate your input."

    player: Optional[DeadlockedPlayer] = session.query(DeadlockedPlayer).filter_by(horizon_id=int(player_id)).first()

    if player is None:
        player = DeadlockedPlayer(username=player_name, horizon_id=player_id)
        session.add(player)
        session.commit()

        # TODO This has a lot of code smell, but it's a simple way to ensure the existence of 1-1 tables.
        update_deadlocked_player_vanilla_stats(session, player_id, player_name, wide_stats)
    else:

        for index, stat in enumerate(wide_stats):

            if vanilla_stats_map[index]["table"] == "" or vanilla_stats_map[index]["field"] == "":
                continue

            stats_table_obj = getattr(player, vanilla_stats_map[index]["table"])
            setattr(stats_table_obj, vanilla_stats_map[index]["field"], stat)

        session.add(player)
        session.commit()
