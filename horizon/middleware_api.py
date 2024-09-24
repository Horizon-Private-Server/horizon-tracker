import json
from typing import Optional
import aiohttp
import asyncio
import logging

import requests

logger = logging.getLogger("uvicorn")  # Get the uvicorn logger

def authenticate(protocol: str, host: str, username: str, password: str) -> str:
    """
    Makes an authentication POST request to the Horizon Middleware server to
    exchange a username and password for a JWT Bearer Token.

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param username: Username to authenticate.
    :param password: Password for username.
    :return: The raw JWT Bearer Token.
    """

    authentication_url: str = f"{protocol}://{host}/Account/authenticate"

    authentication_body: dict[str, str] = {
        "AccountName": username,
        "Password": password
    }

    auth_response = requests.post(
        authentication_url,
        json=authentication_body,
        verify=protocol != "https"
    )

    auth_response_json: dict[str, any] = json.loads(auth_response.text)

    return auth_response_json["Token"]


async def authenticate_async(protocol: str, host: str, username: str, password: str) -> str:
    """
    Makes an asynchronous authentication POST request to the Horizon Middleware server
    to exchange a username and password for a JWT Bearer Token.

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param username: Username to authenticate.
    :param password: Password for username.
    :return: The raw JWT Bearer Token.
    """

    authentication_url: str = f"{protocol}://{host}/Account/authenticate"

    authentication_body: dict[str, str] = {
        "AccountName": username,
        "Password": password
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(authentication_url, json=authentication_body, ssl=protocol != "https") as response:
            response_text = await response.text()
            auth_response_json: dict[str, any] = json.loads(response_text)
            return auth_response_json["Token"]


async def get_all_accounts_async(protocol: str, host: str, app_id: str | int, token: str) -> list[dict[str, any]]:
    """
    Makes an asynchronous request to the Horizon Middleware leaderboard API which functionally
    makes a medium-weight list of all users with basic stats.

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param app_id: The Horizon App ID to filter by.
    :param token: The requesting user's authentication token.
    :return: A list of dictionaries representing accounts.
    """
    leaderboard_url: str = f"{protocol}://{host}/Stats/getLeaderboard?StatId={2}&StartIndex={0}&Size={100_000}&AppId={app_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(leaderboard_url, headers={"Authorization": f"Bearer {token}"}, ssl=False) as response:
            if response.status == 200:  # Check if response status code is 200 (OK)
                return await response.json()  # Parse the response as JSON if status is OK
            logger.warning(f"get_all_accounts got {response.status} from {protocol}://{host}")
            return []


async def get_account_basic_stats_async(protocol: str, host: str, account_id: str | int, app_id: str | int, token: str) -> Optional[dict[str, any]]:
    """
    Makes a request to the Horizon Middleware account API which returns
    all basic stats for a user (including vanilla and custom stats).

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param account_id: The Horizon Account ID to lookup for detailed stats.
    :param app_id: The Horizon App ID to filter by.
    :param token: The requesting user's authentication token.
    :return:
    """
    account_url = f"{protocol}://{host}/Account/getAccountBasic?AccountId={account_id}&AppId={app_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(account_url, headers={"Authorization": f"Bearer {token}"}, ssl=False) as response:
            if response.status == 200:
                return await response.json()  # Parse the response as JSON if status is OK
            logger.warning(f"get_account_basic_stats got {response.status} from {protocol}://{host}")
            return []

async def get_players_online(protocol: str, host: str, token: str) -> list[dict[str, any]]:
    """
    Makes a request to the Horizon Middleware account API which returns
    all players online.

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param token: The requesting user's authentication token.
    :return:
    """
    headers = {"Authorization": f"Bearer {token}"}
    active_games_url = f"{protocol}://{host}/Account/getOnlineAccounts/"
    async with aiohttp.ClientSession() as session:
        async with session.get(active_games_url, headers=headers, ssl=False) as response:
            if response.status == 200:  # Check if response status code is 200 (OK)
                return await response.json()  # Parse the response as JSON if status is OK
            
            logger.warning(f"get_players_online got {response.status} from {protocol}://{host}")
            return []

async def get_active_games(protocol: str, host: str, token: str) -> list[dict[str, any]]:
    """
    Makes a request to the Horizon Middleware account API which returns
    the active games.

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param token: The requesting user's authentication token.
    :return:
    """
    headers = {"Authorization": f"Bearer {token}"}
    active_games_url = f"{protocol}://{host}/api/Game/list"
    async with aiohttp.ClientSession() as session:
        async with session.get(active_games_url, headers=headers, ssl=False) as response:
            if response.status == 200:  # Check if response status code is 200 (OK)
                return await response.json()  # Parse the response as JSON if status is OK

            logger.warning(f"get_active_games got {response.status} from {protocol}://{host}")
            return []

async def get_recent_stats(protocol: str, host: str, token: str, minutes: int=5) -> list[dict[str, any]]:
    """
    Makes a request to the Horizon Middleware account API which returns
    a list of [{account_id: {stat_id: stat_value}}]

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param token: The requesting user's authentication token.
    :param minutes: How many minutes ago to consider 'recent' (max of 60)
    :return:
    """
    headers = {"Authorization": f"Bearer {token}"}
    active_games_url = f"{protocol}://{host}/Stats/getRecentStatChanges?minutes={minutes}"
    async with aiohttp.ClientSession() as session:
        async with session.get(active_games_url, headers=headers, ssl=False) as response:
            if response.status == 200:  # Check if response status code is 200 (OK)
                return await response.json()  # Parse the response as JSON if status is OK

            logger.warning(f"get_recent_stats got {response.status} from {protocol}://{host}")
            return []


async def get_recent_game_history(protocol: str, host: str, token: str, app_id: int, minutes: int=5) -> list[dict[str, any]]:
    """
    Makes a request to the Horizon Middleware account API which returns
    a list of raw game values.

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param app_id: The Horizon App ID to filter by.
    :param token: The requesting user's authentication token.
    :param minutes: How many minutes ago to consider 'recent' (max of 60)
    :return:
    """
    headers = {"Authorization": f"Bearer {token}"}
    active_games_url = f"{protocol}://{host}/api/Game/history/getRecentGames?appId={app_id}&minutes={minutes}"
    async with aiohttp.ClientSession() as session:
        async with session.get(active_games_url, headers=headers, ssl=False) as response:
            if response.status == 200:  # Check if response status code is 200 (OK)
                return await response.json()  # Parse the response as JSON if status is OK

            logger.warning(f"get_recent_game_history got {response.status} from {protocol}://{host}")
            return []




#########################################################################
#                  Code for ad-hoc syncing to database                  #
#########################################################################

def get_all_accounts(protocol: str, host: str, app_id: str | int, token: str) -> list[dict[str, any]]:
    """
    Makes a request to the Horizon Middleware leaderboard API which functionally
    make a medium-weight list of all users with basic stats.

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param app_id: The Horizon App ID to filter by.
    :param token: The requesting user's authentication token.
    :return:
    """
    leaderboard_url: str = f"{protocol}://{host}/Stats/getLeaderboard?StatId={2}&StartIndex={0}&Size={100_000}&AppId={app_id}"

    leaderboard_response = requests.get(leaderboard_url, headers={"Authorization": f"Bearer {token}"}, verify=False)
    return json.loads(leaderboard_response.text)


def get_account_basic_stats(protocol: str, host: str, account_id: str | int, app_id: str | int, token: str) -> Optional[dict[str, any]]:
    """
    Makes a request to the Horizon Middleware account API which returns
    all basic stats for a user (including vanilla and custom stats).

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param account_id: The Horizon Account ID to lookup for detailed stats.
    :param app_id: The Horizon App ID to filter by.
    :param token: The requesting user's authentication token.
    :return:
    """
    account_url = f"{protocol}://{host}/Account/getAccountBasic?AccountId={account_id}&AppId={app_id}"
    account_response = requests.get(account_url, headers={"Authorization": f"Bearer {token}"}, verify=False)

    if account_response.status_code != 200:
        return None

    return json.loads(account_response.text)


def get_all_game_history(protocol: str, host: str, app_id: str | int, token: str, game_end:str = '2024-09-19T15:36:54') -> Optional[dict[str, any]]:
    """
    Make a series of requests to get all game history.

    :param protocol: "HTTP" or "HTTPS".
    :param host: Host name and optional port of the target Horizon Middleware server
        (i.e., "stats.rac-horizon.com" or "111.222.111.222:1234").
    :param account_id: The Horizon Account ID to lookup for detailed stats.
    :param app_id: The Horizon App ID to filter by.
    :param token: The requesting user's authentication token.
    :param game_end: The end time for the last record returned
    :return:
    """
    print("Downloading game history ...")
    counter = 1
    results = []
    while True:
        url = f"{protocol}://{host}/api/Game/historyByDate/{app_id}?lastGameEndDt={game_end}"
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, verify=False)

        if counter % 10 == 0:
            print(f"Processed {counter*100} games...")

        if response.status_code != 200:
            logger.warning(f"get_game_history got {response.status_code} from {protocol}://{host}")
            return results

        result = json.loads(response.text)
        if len(result) == 0:
            return results
        
        results += result["Games"]
        counter += 1

        game_end = result["NextCursor"]
