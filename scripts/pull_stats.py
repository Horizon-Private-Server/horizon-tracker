"""
This script connects to the prod Horizon Middleware and dumps the full stats of each player into a JSON file.
"""
import json
import os
from asyncio import Future
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta

from tqdm import tqdm

from app.database import CREDENTIALS

from horizon.middleware_api import (
    authenticate,
    get_all_accounts,
    get_account_basic_stats,
    get_all_game_history
)

# Prevent requests from spamming to the console.
import urllib3
urllib3.disable_warnings()

if __name__ == "__main__":

    os.makedirs("data", exist_ok=True)

    for game in ("uya", "dl"):
        protocol: str = CREDENTIALS[game]["horizon_middleware_protocol"]
        host: str = CREDENTIALS[game]["horizon_middleware_host"]
        horizon_app_id_ntsc: int = CREDENTIALS[game]["horizon_app_id_ntsc"]
        horizon_username: str = CREDENTIALS[game]["horizon_middleware_username"]
        horizon_password: str = CREDENTIALS[game]["horizon_middleware_password"]

        token: str = authenticate(
            protocol=protocol,
            host=host,
            username=horizon_username,
            password=horizon_password
        )

        for game_version in ("ntsc", "pal"):
            app_id = CREDENTIALS[game][f"horizon_app_id_{game_version}"]

            # Process player stats
            all_players: list[dict[str, any]] = get_all_accounts(
                protocol=protocol,
                host=host,
                app_id=app_id,
                token=token
            )

            all_stats: dict = dict()

            start_time: datetime = datetime.now()

            def pull_player_full_stats(player_id: int):
                all_stats[player_id] = get_account_basic_stats(
                    protocol=protocol,
                    host=host,
                    account_id=player_id,
                    app_id=app_id,
                    token=token
                )

            with ThreadPoolExecutor(max_workers=10) as executor:
                # List operation is needed to collapse tqdm into a one-liner. This has minimal performance impact.
                list(tqdm(
                    executor.map(pull_player_full_stats, map(lambda _player: _player["AccountId"], all_players)), total=len(all_players),
                    desc=f"Pulling stats from {game.upper()} ({game_version.upper()}) Horizon Production..."
                ))

            time_taken: timedelta = datetime.now() - start_time
            minutes, seconds = divmod(time_taken.total_seconds(), 60)
            print(f"Time taken: {int(minutes)} minutes and {seconds:.2f} seconds")

            with open(f"data/{game}_stats_{game_version}.json", "w") as stream:
                json.dump(all_stats, stream)

        # Process game history
        game_history: list[dict] = get_all_game_history(protocol, host, horizon_app_id_ntsc, token, str(datetime.now()))
        with open(f"data/{game}_gamehistory.json", "w") as stream:
            json.dump(game_history, stream)
