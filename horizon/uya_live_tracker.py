import os
import logging
import asyncio
import json

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


class UyaLiveTracker():
    def __init__(self, port:int=8888, read_tick_rate:int=5, write_tick_rate:int=5, read_games_api_rate:int=10):
        self._backend = LiveTrackerBackend(server_ip=os.getenv('SOCKET_IP'), log_level='INFO')
        self._ip = '0.0.0.0'
        self._port = port

        # In seconds
        self._read_games_api_rate = read_games_api_rate

        # Ticks per second
        self._read_tick_rate = read_tick_rate / 60
        self._write_tick_rate = write_tick_rate / 60

        self._world_state = []
        self._games = dict()

        self._active_connections: list[WebSocket] = []

    def add_connection(self, websocket: WebSocket):
        self._active_connections.append(websocket)

    def remove_connection(self, websocket: WebSocket):
        self._active_connections.remove(websocket)

    async def write(self, websocket: WebSocket):
        data = json.dumps([world_state.dict() for world_state in self._world_state])
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
        if map == 'Bakisi Isles':
            xmin = 11745
            xmax = 39504
            ymin = 13133
            ymax = 38565
        elif map == 'Hoven Gorge':
            xmin = 8391
            xmax = 24448
            ymin = 7380
            ymax = 25070

        # Convert the coordinates to between 0 and 100
        # Do 100- on y so that it's reversed (canvas in front end expects top left to be 0,0)
        new_coord = list(coord)
        new_coord[0] = ((coord[0] - xmin) / (xmax - xmin)) * 100
        new_coord[1] = 100 - ((coord[1] - ymin) / (ymax - ymin)) * 100

        return tuple(new_coord)

uya_live_tracker = UyaLiveTracker()