import asyncio

from fastapi import APIRouter, Depends

from app.constants.message import MessageStatus
from app.models.message import TransationResponse, UserAnswerInput
from app.usecases.wellness_assistant_usecase import WellnessUsecase

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
async def initialize(
    session_id: str,
    wellness_usecase: WellnessUsecase = Depends(WellnessUsecase),
) -> TransationResponse:
    asyncio.create_task(wellness_usecase.initialize_session(session_id))
    return TransationResponse(status=MessageStatus.SUCCESS, message='Wellness Profile Initialized')


@wellness_profile.post(
    '/userAnswer/{session_id}',
    response_model=TransationResponse,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    description='User answer to the wellness profile question',
    summary='User answer to the wellness profile question',
    tags=['Wellness Profile'],
)
async def user_answer(
    session_id: str,
    message: UserAnswerInput,
    wellness_usecase: WellnessUsecase = Depends(WellnessUsecase),
) -> TransationResponse:
    asyncio.create_task(wellness_usecase.send_message_to_assistant(session_id, message))
    return TransationResponse(status=MessageStatus.SUCCESS, message='User Answer Sent')
