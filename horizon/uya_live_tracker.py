import os
import logging
import asyncio
import json
from collections import deque
from datetime import datetime, timedelta
from copy import deepcopy

from livetrackerbackend import LiveTrackerBackend
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
        self._backend = LiveTrackerBackend(server_ip=CREDENTIALS["uya"]["live_tracker_socket_ip"], log_level='INFO')
        self._ip = '0.0.0.0'
        self._port = port

        # In seconds
        self._read_games_api_rate = read_games_api_rate

        # Ticks per second
        self._read_tick_rate = 1 / read_tick_rate
        self._write_tick_rate = 1 / write_tick_rate
        self._world_state = []
        self._world_state_history = deque(maxlen=350) # For automatic popping so we don't need to remove. Prevents memory leaks too
        self._games = dict()

        self._active_connections: list[WebSocket] = []

        # Delay in seconds for writing to the websocket to prevent cheating
        self._write_delay = write_delay

        with open(os.path.join("horizon","parsing","uya_live_map_boundaries.json"), "r") as f:
            self._transform_coord_map = json.loads(f.read())

    def add_connection(self, websocket: WebSocket):
        self._active_connections.append(websocket)

    def remove_connection(self, websocket: WebSocket):
        self._active_connections.remove(websocket)

    async def write(self, websocket: WebSocket):
        """Return the world state from _delay_ seconds ago, if available."""
        current_time = datetime.now()
        delay_threshold = current_time - timedelta(seconds=self._write_delay)
        
        worlds = []
        # Check the deque for the most recent state that is exactly write_delay seconds old or newer
        # Will almost always be the first in the deque (good performance)
        for ts, state in self._world_state_history:
            if ts <= delay_threshold:
                worlds = state
                break

        data = json.dumps([world_state.dict() for world_state in worlds])
        await websocket.send_text(data)
        await asyncio.sleep(self._write_tick_rate)

    async def start(self, loop):
        # Read from the prod uya live socket
        self._backend.start(loop)

        loop.create_task(self.read_prod_socket())
        loop.create_task(self.read_games_api())

    async def read_prod_socket(self):
        while True:
            try:
                worlds:list[dict] = self._backend.get_world_states()
                worlds = [UYALiveGameSession(**world) for world in worlds]
                self._world_state = []

                for world in worlds:
                    if world.world_id not in self._games.keys():
                        continue
                    game = self._games[world.world_id]

                    world.map = game.map
                    world.name = game.name
                    world.game_mode = game.game_mode

                    world_players = list(sorted(world.players, key=lambda player: player.player_id))
                    game_players = game.players
                    for idx in range(min(len(world_players), len(game_players))):
                        #world_players[idx].username = world_players[idx].username
                        world_players[idx].coord = self.transform_coord(world.map, world_players[idx].coord)
                    world.players = world_players

                    self._world_state.append(world)

                self._world_state_history.append((datetime.now(), deepcopy(self._world_state)))
            
            except Exception as e:
                logger.error("read_prod_socket failed to update!", exc_info=True)

            await asyncio.sleep(self._read_tick_rate)

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