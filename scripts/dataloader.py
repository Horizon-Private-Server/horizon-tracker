"""
This script dataloads the Postgres database from a JSON output.
"""
import json

from tqdm import tqdm

from app.database import SessionLocal
from app.utils.query_helpers import update_deadlocked_player_vanilla_stats, update_deadlocked_player_custom_stats

if __name__ == "__main__":

    with open("stats.json") as stream:
        all_stats: dict[str, dict] = json.load(stream)

    for account_id in tqdm(all_stats, desc="Ingesting data into Postgres..."):
        account_full = all_stats[account_id]

        update_deadlocked_player_vanilla_stats(
            session=SessionLocal(),
            player_id=account_id,
            player_name=account_full["AccountName"],
            wide_stats=account_full["AccountWideStats"]
        )

        update_deadlocked_player_custom_stats(
            session=SessionLocal(),
            player_id=account_id,
            player_name=account_full["AccountName"],
            wide_custom_stats=account_full["AccountCustomWideStats"]
        )
