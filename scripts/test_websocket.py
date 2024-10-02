import asyncio
import websockets

async def read_websocket():
    uri = f"ws://localhost:8888"
    async with websockets.connect(uri,ping_interval=None) as websocket:
        while True:
            data = await websocket.recv()
            print(data)


asyncio.new_event_loop().run_until_complete(read_websocket())