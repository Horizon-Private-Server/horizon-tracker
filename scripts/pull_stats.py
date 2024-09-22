"""
This script connects to the prod Horizon Middleware and dumps the full stats of each player into a JSON file.
"""
import json
from datetime import datetime, timedelta

from tqdm import tqdm

from app.database import CREDENTIALS

from horizon.middleware_api import (
    authenticate,
    get_all_accounts,
    get_account_basic_stats
)

# Prevent requests from spamming to the console.
import urllib3
urllib3.disable_warnings()

if __name__ == "__main__":
    for game in ("uya", "dl"):
        protocol: str = CREDENTIALS[game]["horizon_middleware_protocol"]
        host: str = CREDENTIALS[game]["horizon_middleware_host"]
        horizon_app_id: int = CREDENTIALS[game]["horizon_app_id"]
        horizon_username: str = CREDENTIALS[game]["horizon_middleware_username"]
        horizon_password: str = CREDENTIALS[game]["horizon_middleware_password"]

        token: str = authenticate(
            protocol=protocol,
            host=host,
            username=horizon_username,
            password=horizon_password
        )

        all_players: list[dict[str, any]] = get_all_accounts(
            protocol=protocol,
            host=host,
            app_id=horizon_app_id,
            token=token
        )

        all_stats: dict = dict()

        start_time: datetime = datetime.now()
        for leaderboard_item in tqdm(all_players, desc=f"Pulling stats from {game.upper()} Horizon Production..."):
            all_stats[leaderboard_item["AccountId"]] = get_account_basic_stats(
                protocol=protocol,
                host=host,
                account_id=leaderboard_item["AccountId"],
                app_id=horizon_app_id,
                token=token
            )
        time_taken: timedelta = datetime.now() - start_time
        minutes, seconds = divmod(time_taken.total_seconds(), 60)
        print(f"Time taken: {int(minutes)} minutes and {seconds:.2f} seconds")

        with open(f"{game}_stats.json", "w") as stream:
            json.dump(all_stats, stream)
