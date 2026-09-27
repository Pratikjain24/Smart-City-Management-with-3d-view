import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.config import settings
from app.services.telemetry_simulator import telemetry_hub

router = APIRouter()
logger = logging.getLogger("mahatwin.ws")

@router.websocket("/live-stream")
async def websocket_live_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected to MahaTwin Live Telemetry Stream")

    # Optional Redis Pub/Sub support
    redis_client = None
    try:
        import redis.asyncio as aioredis
        if settings.REDIS_URL:
            r = aioredis.from_url(settings.REDIS_URL, socket_connect_timeout=0.5)
            # Test ping
            await asyncio.wait_for(r.ping(), timeout=0.5)
            redis_client = r
            logger.info("Live telemetry stream connected with Redis Pub/Sub event broker")
    except Exception:
        # Fallback to local high-precision telemetry loop
        redis_client = None

    try:
        while True:
            # Emit live synchronized telemetry pulse every 1 second
            tick_data = telemetry_hub.get_live_tick()

            # If redis is active, publish tick to broker
            if redis_client:
                try:
                    await redis_client.publish("mahatwin:telemetry", json.dumps(tick_data))
                except Exception as pub_err:
                    logger.debug(f"Redis publish notice: {pub_err}")

            await websocket.send_json(tick_data)
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        logger.info("Client disconnected from Live Telemetry Stream")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except Exception:
            pass
    finally:
        if redis_client:
            try:
                await redis_client.close()
            except Exception:
                pass
