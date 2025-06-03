from fastapi import APIRouter

from app.constants.message import MessageStatus
from app.models.message import TransationResponse
from app.repositories.shared_state import get_connection_manager

wellness_profile = APIRouter()


@wellness_profile.post(
    '/initialize/{session_id}',
    response_model=TransationResponse,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    description='Initialize the wellness profile session',
    summary='Initialize the wellness profile session',
    tags=['Wellness Profile'],
)
async def initialize(session_id: str) -> TransationResponse:
    manager = get_connection_manager()
    connections = manager.get_connections_with_session_id(session_id)
    if not connections:
        return TransationResponse(
            status=MessageStatus.ERROR, message='No connection found for session'
        )

    for connection in connections:
        await manager.send_personal_message(
            'Wellness profile session initialized via REST API',
            connection,
        )

    return TransationResponse(status=MessageStatus.SUCCESS, message='Wellness profile initialized')


@wellness_profile.post(
    '/userAnswer',
)
async def user_answer(session_id: str):
    return {'message': 'Wellness profile'}


@wellness_profile.get('/status')
async def get_wellness_profile(session_id: str):
    return {'message': 'Wellness profile'}
