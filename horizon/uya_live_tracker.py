import os
import logging
import asyncio
import json
from collections import deque
from datetime import datetime, timedelta
from copy import deepcopy
import websockets

from fastapi import WebSocket

from livetrackerserver import UyaLiveTracker as UyaLiveTrackerServer


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

from app.utils.general import read_environment_variables

CREDENTIALS: dict[str, any] = read_environment_variables()


class UyaLiveTracker:
    def __init__(self, port: int = 8888, read_tick_rate: int = 10, write_tick_rate: int = 10, read_games_api_rate: int = 10, write_delay: int = 30):
        self._simulated = CREDENTIALS["uya"]["live_tracker_simulated"]
        self._ip = '0.0.0.0'
        self._port = port

        self._tracker = None
        self._worlds = '[]'
        self._active_connections: list[WebSocket] = []

        self._read_tick_rate = 1 / read_tick_rate
        self._write_tick_rate = 1 / write_tick_rate

    ####### READ FROM PROD METHODS
    async def read_prod_websocket(self):
        while True:
            try:
                while True:
                    self._worlds = self._tracker.dump()
                    #print(datetime.now(), "got world:", self._worlds)
                    await asyncio.sleep(.01)
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
        await websocket.send_text(self._worlds)
        await asyncio.sleep(self._write_tick_rate)

    async def start(self, loop):
        self._tracker = UyaLiveTrackerServer(loop, CREDENTIALS["uya"]["live_tracker_socket_ip"], CREDENTIALS["uya"]["horizon_middleware_protocol"], CREDENTIALS["uya"]["horizon_middleware_host"], CREDENTIALS["uya"]["horizon_middleware_username"], CREDENTIALS["uya"]["horizon_middleware_password"])
        await self._tracker.start()
        loop.create_task(self.read_prod_websocket())

uya_live_tracker: UyaLiveTracker = UyaLiveTracker()
