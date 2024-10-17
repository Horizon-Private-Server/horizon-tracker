import asyncio
import websockets
from datetime import datetime

async def read_websocket():
    uri = f"ws://localhost:8000/uya-live-ws"
    while True:
        try:
            async with websockets.connect(uri,ping_interval=None) as websocket:
                while True:
                    data = await websocket.recv()
                    print(datetime.now(), data)
        except Exception as e:
            print(f"Unable to connect: {e}")
            await asyncio.sleep(5)

asyncio.new_event_loop().run_until_complete(read_websocket())
