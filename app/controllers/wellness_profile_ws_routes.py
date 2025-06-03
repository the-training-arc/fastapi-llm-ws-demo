from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from structlog import get_logger

from app.constants.message import MessageEvent
from app.models.message import Message
from app.repositories.shared_state import (
    get_connection_manager,
    session_messages,
    session_status,
    session_wellness_confidence,
    session_wellness_profiles,
)
from app.usecases.wellness_assistant_usecase import WellnessAssistantUsecase

ws_routes = APIRouter()


@ws_routes.websocket('/wellness_profile/{session_id}')
async def wellness_profile(
    websocket: WebSocket,
    session_id: str,
    manager=Depends(get_connection_manager),
):
    logger = get_logger()
    await manager.connect(websocket, session_id)

    try:
        while True:
            data = await websocket.receive_json()
            if not data:
                continue

            try:
                message = Message(**data)
            except ValidationError as e:
                logger.error('Invalid message', session_id=session_id, error=e)
                await manager.send_personal_message(f'Invalid message: {e}', websocket)
                continue

            manager.store_message(session_id, message.model_dump())

            wellness_assistant_usecase = WellnessAssistantUsecase(websocket, manager)
            await wellness_assistant_usecase.start_profiling(
                session_id,
                message,
                session_status,
                session_wellness_profiles,
                session_wellness_confidence,
                session_messages,
            )

    except WebSocketDisconnect as e:
        message = f'Client disconnected: {str(e)}'
        logger.error(message, session_id=session_id)
        manager.disconnect(websocket)

        # Clean up session data
        session_wellness_profiles.pop(session_id, None)
        session_wellness_confidence.pop(session_id, None)

    except Exception as e:
        message = f'Error in wellness profile: {str(e)}'
        logger.error(message, session_id=session_id)
        response = Message(event=MessageEvent.ASSISTANT_QUESTION, message=message)
        await manager.send_personal_message(response.model_dump_json(), websocket)
