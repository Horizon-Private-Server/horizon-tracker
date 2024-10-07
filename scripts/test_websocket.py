import asyncio
import websockets

async def read_websocket():
    uri = f"ws://localhost:8888"
    while True:
        try:
            async with websockets.connect(uri,ping_interval=None) as websocket:
                while True:
                    data = await websocket.recv()
                    print(data)
        except:
            print("Unable to connect!")
            await asyncio.sleep(5)

asyncio.new_event_loop().run_until_complete(read_websocket())