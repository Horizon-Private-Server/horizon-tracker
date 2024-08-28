"""
This script dataloads the Postgres database from a JSON output.
"""
import json
from typing import Dict

from tqdm import tqdm

from app.database import SessionLocal
from app.utils.query_helpers import update_deadlocked_player_vanilla_stats

if __name__ == "__main__":

    with open("stats.json") as stream:
        all_stats: Dict[str, Dict] = json.load(stream)

    for account_id in tqdm(all_stats, desc="Ingesting data into Postgres..."):
        account_full = all_stats[account_id]

        update_deadlocked_player_vanilla_stats(
            session=SessionLocal(),
            player_id=account_id,
            player_name=account_full["AccountName"],
            wide_stats=account_full["AccountWideStats"]
        )
