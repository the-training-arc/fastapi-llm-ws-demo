from typing import Dict, List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from structlog import get_logger

from app.constants.message import MessageEvent
from app.constants.profiling_stage import ProfilingStage, ProfilingStageMapping
from app.constants.questions import WellnessProfileQuestions
from app.models.message import Message
from app.usecases.llm_usecase import LLMUsecase
from app.usecases.session_manager_usecase import ConnectionManager

ws_routes = APIRouter()

session_messages: Dict[str, List[dict]] = {}
session_status: Dict[str, ProfilingStage] = {}


@ws_routes.websocket('/wellness_profile/{session_id}')
async def wellness_profile(
    websocket: WebSocket,
    session_id: str,
    llm_usecase: LLMUsecase = Depends(LLMUsecase),
    manager: ConnectionManager = Depends(lambda: ConnectionManager(session_messages)),
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

            current_stage = session_status.get(session_id, ProfilingStage.INTRODUCTION)

            if (
                message.event == MessageEvent.INIT_PROFILE.value
                or current_stage == ProfilingStage.INTRODUCTION
            ):
                response = Message(
                    event=MessageEvent.ASSISTANT_QUESTION,
                    message=WellnessProfileQuestions.INTRODUCTION,
                )
                await manager.send_personal_message(
                    response.model_dump_json(), websocket, persist=True
                )

                next_stage = ProfilingStageMapping.get_next_stage(current_stage)
                session_status[session_id] = next_stage

            elif message.event == MessageEvent.USER_ANSWER.value:
                response = llm_usecase.get_output_model_from_user_response(
                    message.message, WellnessProfileQuestions.INTRODUCTION
                )
                await manager.send_personal_message(
                    response.model_dump_json(), websocket, persist=True
                )

    except WebSocketDisconnect as e:
        message = f'Client disconnected: {str(e)}'
        logger.error(message, session_id=session_id)
        manager.disconnect(websocket)

    except Exception as e:
        message = f'Error in wellness profile: {str(e)}'
        logger.error(message, session_id=session_id)
        response = Message(event=MessageEvent.ASSISTANT_QUESTION, message=message)
        await manager.send_personal_message(response.model_dump_json(), websocket)
