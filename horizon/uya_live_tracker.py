import os
import logging
import asyncio
import json
from collections import deque
from datetime import datetime, timedelta
from copy import deepcopy
import websockets

from fastapi import WebSocket

from horizon.middleware_manager import uya_online_tracker
from app.schemas.schemas import UYALiveGameSession

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

from app.utils.general import read_environment_variables

CREDENTIALS: dict[str, any] = read_environment_variables()

class UyaLiveTracker():
    def __init__(self, port:int=8888, read_tick_rate:int=10, write_tick_rate:int=10, read_games_api_rate:int=10, write_delay:int=30):
        self._simulated = CREDENTIALS["uya"]["live_tracker_simulated"]
        self._ip = '0.0.0.0'
        self._port = port

        self._prod_uri = f"ws://{CREDENTIALS["uya"]["live_tracker_socket_ip"]}:{port}"

        # In seconds
        self._read_games_api_rate = read_games_api_rate

        # Ticks per second
        self._read_tick_rate = 1 / read_tick_rate
        self._write_tick_rate = 1 / write_tick_rate
        self._worlds = []

        self._active_connections: list[WebSocket] = []

        # Delay in seconds for writing to the websocket to prevent cheating
        self._write_delay = write_delay

        with open(os.path.join("horizon","parsing","uya_live_map_boundaries.json"), "r") as f:
            self._transform_coord_map = json.loads(f.read())


    ####### READ FROM PROD METHODS
    async def read_prod_websocket(self):
        while True:
            try:
                async with websockets.connect(self._prod_uri,ping_interval=None) as websocket:
                    while True:
                        data = await websocket.recv()
                        self._worlds = [UYALiveGameSession(**world) for world in json.loads(data)]
            except Exception as e:
                logger.warning(f"read_prod_websocket: Unable to connect", exc_info=True)
                await asyncio.sleep(5)

    ####### PUSHING TO CLIENTS METHODS
    def add_connection(self, websocket: WebSocket):
        self._active_connections.append(websocket)

    def remove_connection(self, websocket: WebSocket):
        self._active_connections.remove(websocket)

    async def write(self, websocket: WebSocket):
        """Return the world state from _delay_ seconds ago, if available."""
        data = json.dumps([world_state.dict() for world_state in self._worlds])
        await websocket.send_text(data)
        await asyncio.sleep(self._write_tick_rate)

    async def start(self, loop):
        loop.create_task(self.read_prod_websocket())
        loop.create_task(self.read_games_api())

    async def read_games_api(self):
        while True:
            try:
                games = uya_online_tracker.get_games()
                self._games = {game.id-1: game for game in games}
            except Exception as e:
                logger.error("read_games_api failed to update!", exc_info=True)
            await asyncio.sleep(self._read_games_api_rate)

    def transform_coord(self, map:str, coord:tuple):
        if map not in self._transform_coord_map.keys():
            return [50,50]

        min_maxes:dict = self._transform_coord_map[map]
        new_coord = list(coord)
        new_coord[0] = ((coord[0] - min_maxes["xmin"]) / (min_maxes["xmax"] - min_maxes["xmin"])) * 100
        new_coord[1] = 100 - ((coord[1] - min_maxes["ymin"]) / (min_maxes["ymax"] - min_maxes["ymin"])) * 100

        return tuple(new_coord)

uya_live_tracker = UyaLiveTracker()