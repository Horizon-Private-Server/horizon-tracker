import os
import logging
import asyncio
from time import sleep
import json
from logging import handlers
from datetime import datetime
from livetrackerbackend import LiveTrackerBackend

from horizon.middleware_manager import uya_online_tracker


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

import websockets


class UyaLiveTracker():
    def __init__(self, port:int=8888, read_tick_rate:int=60, write_tick_rate:int=15, read_games_api_rate:int=10):

        self._backend = LiveTrackerBackend(server_ip=os.getenv('SOCKET_IP'), log_level='INFO')
        self._ip = '0.0.0.0'
        self._port = port

        self._connected = set()

        # In seconds
        self._read_games_api_rate = read_games_api_rate

        # Ticks per second
        self._read_tick_rate = read_tick_rate / 60
        self._write_tick_rate = write_tick_rate / 60

        self._world_state = []
        self._games = dict()


    async def start(self, loop):
        self._backend.start(loop)
        await self.start_websocket()

        loop.create_task(self.read_prod_socket())
        loop.create_task(self.read_games_api())
        loop.create_task(self.flush())

    async def start_websocket(self):
        await websockets.serve(self.on_websocket_connection, '0.0.0.0', self._port)
        logger.info(f"Websocket serving on ('0.0.0.0', {self._port}) ...")

    async def read_prod_socket(self):
        while True:
            try:
                worlds:list[dict] = self._backend.get_world_states()
                self._world_state = []

                for world in worlds:
                    if world["world_id"] not in self._games.keys():
                        continue
                    game = self._games[world["world_id"]]

                    world_players = list(sorted(world["players"], key=lambda player: player["player_id"]))
                    game_players = game.players
                    for idx in range(min(len(world_players), len(game_players))):
                        world_players[idx]["username"] = game_players[idx].username

                    world["players"] = world_players
                    world["map"] = game.map
                    world["name"] = game.name
                    world["game_mode"] = game.game_mode
                    self._world_state.append(world)


            except Exception as e:
                logger.error("read_prod_socket failed to update!", exc_info=True)

            await asyncio.sleep(self._read_tick_rate)

    async def flush(self):
        while True:
            try:
                data = json.dumps(self._world_state)

                if len(self._connected) > 0:
                    for connection in self._connected:
                        try:
                            await connection.send(data)
                        except Exception:
                            connection.connected = False
            except Exception as e:
                logger.error("flush failed to update!", exc_info=True)

            await asyncio.sleep(self._write_tick_rate)

    async def read_games_api(self):
        while True:
            try:
                games = uya_online_tracker.get_games()
                self._games = {game.id-1: game for game in games}
            except Exception as e:
                logger.error("read_games_api failed to update!", exc_info=True)
            await asyncio.sleep(self._read_games_api_rate)

    async def on_websocket_connection(self, websocket, path):
        logger.info(f"Websocket client connected: {websocket.remote_address}")
        # Register.
        self._connected.add(websocket)
        websocket.connected = True
        try:
            while websocket.connected:
                await asyncio.sleep(.001)
        finally:
            logger.info("Websocket disconnected!")
            # Unregister.
            self._connected.remove(websocket)


uya_live_tracker = UyaLiveTracker()