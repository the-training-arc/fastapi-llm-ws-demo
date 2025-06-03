from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from structlog import get_logger

from app.repositories.shared_state import (
    get_connection_manager,
)

ws_routes = APIRouter()


@ws_routes.websocket('/wellnessProfile/{session_id}')
async def wellness_profile(
    websocket: WebSocket,
    session_id: str,
    manager=Depends(get_connection_manager),
):
    logger = get_logger()
    await manager.connect(websocket, session_id)

    try:
        await websocket.receive_text()

    except WebSocketDisconnect as e:
        message = f'Client disconnected: {str(e)}'
        logger.error(message, session_id=session_id)
        manager.disconnect(websocket)

    except Exception as e:
        message = f'Error in wellness profile: {str(e)}'
        logger.error(message, session_id=session_id)
        manager.disconnect(websocket)
