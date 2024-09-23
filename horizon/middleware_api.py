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


async def get_players_online(protocol: str, host: str, token: str) -> Optional[dict[str, any]]:
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

async def get_active_games(protocol: str, host: str, token: str) -> Optional[dict[str, any]]:
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