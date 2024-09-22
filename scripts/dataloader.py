"""
This script dataloads the Postgres database from a JSON output.
"""
import json
from datetime import datetime, timedelta

from tqdm import tqdm

from app.database import SessionLocal
from app.utils.query_helpers import update_player_vanilla_stats, update_deadlocked_player_custom_stats

if __name__ == "__main__":


    ### UYA
    start_time = datetime.now()
    with open("uya_stats.json") as stream:
        all_stats: dict[str, dict] = json.load(stream)

    for account_id in tqdm(all_stats, desc="Ingesting UYA data into Postgres..."):
        account_full = all_stats[account_id]

        update_player_vanilla_stats(
            'uya',
            session=SessionLocal(),
            player_id=account_id,
            player_name=account_full["AccountName"],
            wide_stats=account_full["AccountWideStats"]
        )
    time_taken = datetime.now() - start_time
    minutes, seconds = divmod(time_taken.total_seconds(), 60)
    print(f"Time taken: {int(minutes)} minutes and {seconds:.2f} seconds")


    ### DL
    start_time: datetime = datetime.now()
    with open("dl_stats.json") as stream:
        all_stats: dict[str, dict] = json.load(stream)

    for account_id in tqdm(all_stats, desc="Ingesting DL data into Postgres..."):
        account_full = all_stats[account_id]

        update_player_vanilla_stats(
            'dl',
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
    time_taken: timedelta = datetime.now() - start_time
    minutes, seconds = divmod(time_taken.total_seconds(), 60)
    print(f"Time taken: {int(minutes)} minutes and {seconds:.2f} seconds")