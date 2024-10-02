import os
import logging
import asyncio
from time import sleep
import json
from logging import handlers
from datetime import datetime
from livetrackerbackend import LiveTrackerBackend

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

import websockets


class UyaLiveTracker():
    def __init__(self, port:int=8888, read_tick_rate:int=60, write_tick_rate:int=15):

        self._backend = LiveTrackerBackend(server_ip=os.getenv('SOCKET_IP'), log_level='INFO')
        self._ip = '0.0.0.0'
        self._port = port

        self._connected = set()

        # Ticks per second
        self._read_tick_rate = read_tick_rate / 60
        self._write_tick_rate = write_tick_rate / 60

        self._world_state = []


    async def start(self, loop):
        self._backend.start(loop)
        await self.start_websocket()

        loop.create_task(self.read_prod_socket())
        loop.create_task(self.flush())

    async def start_websocket(self):
        await websockets.serve(self.on_websocket_connection, '0.0.0.0', self._port)
        logger.info(f"Websocket serving on ('0.0.0.0', {self._port}) ...")

    async def read_prod_socket(self):
        while True:
            try:
                self._world_state = self._backend.get_world_states()
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