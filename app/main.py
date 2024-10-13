import asyncio
import traceback

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal

from app.routers.dl.stats import router as deadlocked_stats_router
from app.routers.uya.stats import router as uya_stats_router

from app.routers.dl.online import router as deadlocked_online_router
from app.routers.uya.online import router as uya_online_router


from app.routers.uya.game_history import router as uya_gamehistory_router

from horizon.middleware_manager import uya_online_tracker
from horizon.middleware_manager import dl_online_tracker

from horizon.uya_live_tracker import uya_live_tracker


ALLOWED_ORIGINS: list[str] = [
    "https://www.rac-horizon.com",
    "https://rac-horizon.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add background tasks
@app.on_event("startup")
async def start_background_tasks():
    await uya_live_tracker.start(asyncio.get_event_loop())

    asyncio.create_task(uya_online_tracker.refresh_token())
    asyncio.create_task(uya_online_tracker.update_recent_stat_changes())
    asyncio.create_task(uya_online_tracker.poll_active_online())
    asyncio.create_task(uya_online_tracker.update_recent_game_history())
    asyncio.create_task(dl_online_tracker.refresh_token())
    # asyncio.create_task(dl_online_tracker.update_recent_stat_changes())    # Will work once DL middleware is updated
    asyncio.create_task(dl_online_tracker.poll_active_online())


# Add sub-APIs.
app.include_router(deadlocked_stats_router)
app.include_router(uya_stats_router)
app.include_router(deadlocked_online_router)
app.include_router(uya_online_router)
app.include_router(uya_gamehistory_router)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """
    The following view is designed for sanity checks to ensure that the API is functional.
    """
    return {"message": "Hello World"}


@app.websocket("/uya-live-ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    uya_live_tracker.add_connection(websocket)
    try:
        while True:
            await uya_live_tracker.write(websocket)
    except Exception as e:
        error_type = type(e).__name__  # Get the exception type
        print(f"uya-live-ws Error: {error_type}")
    finally:
        uya_live_tracker.remove_connection(websocket)
