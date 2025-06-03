import json
from typing import Dict, List

from fastapi import WebSocket
from structlog import get_logger

from app.constants.message import MessageEvent
from app.constants.profiling_stage import ProfilingStage, ProfilingStageMapping
from app.constants.questions import WellnessProfileQuestions
from app.constants.wellness_profile import Confidence
from app.models.message import Message
from app.models.wellness_profile import WellnessProfile, WellnessProfileConfidence
from app.usecases.llm_usecase import LLMUsecase
from app.usecases.session_manager_usecase import ConnectionManager


class WellnessAssistantUsecase:
    __slots__ = ('__llm_usecase', '__websocket', '__manager', '__logger')

    def __init__(self, websocket: WebSocket, manager: ConnectionManager):
        self.__llm_usecase = LLMUsecase()
        self.__websocket = websocket
        self.__manager = manager
        self.__logger = get_logger()

    async def start_profiling(
        self,
        session_id: str,
        message: Message,
        session_status: Dict[str, ProfilingStage],
        session_wellness_profiles: Dict[str, WellnessProfile],
        session_wellness_confidence: Dict[str, WellnessProfileConfidence],
        session_messages: Dict[str, List[dict]],
    ):
        current_stage = session_status.get(session_id, ProfilingStage.INIT)

        if (
            message.event == MessageEvent.INIT_PROFILE.value
            or current_stage == ProfilingStage.INIT
        ):
            response = Message(
                event=MessageEvent.ASSISTANT_QUESTION,
                message=WellnessProfileQuestions.INTRODUCTION,
            )
            await self.__manager.send_personal_message(response.model_dump_json(), self.__websocket)

            next_stage = ProfilingStageMapping.get_next_stage(current_stage)
            session_status[session_id] = next_stage

            # Initialize empty wellness profile and confidence for this session
            session_wellness_profiles[session_id] = WellnessProfile()
            session_wellness_confidence[session_id] = WellnessProfileConfidence()

        elif message.event == MessageEvent.USER_ANSWER.value:
            # Get LLM response
            llm_response = self.__llm_usecase.get_output_model_from_user_response(
                message.message,
                WellnessProfileQuestions.INTRODUCTION,
                response_history=session_messages[session_id],
            )

            # Get or initialize existing session data
            existing_profile = session_wellness_profiles.get(session_id, WellnessProfile())
            existing_confidence = session_wellness_confidence.get(
                session_id, WellnessProfileConfidence()
            )

            # Merge new data with existing data
            merged_profile = self.__merge_wellness_profile(
                existing_profile, llm_response.wellnessProfile
            )
            merged_confidence = self.__merge_wellness_confidence(
                existing_confidence, llm_response.confidence
            )

            # Update session state
            session_wellness_profiles[session_id] = merged_profile
            session_wellness_confidence[session_id] = merged_confidence

            # Check if profile is complete
            if self.__is_profile_complete(merged_profile, merged_confidence):
                # Profile is complete - send completion message
                response = Message(
                    event=MessageEvent.PROFILE_COMPLETE,
                    message=json.dumps(merged_profile.model_dump(), indent=4),
                )
                await self.__manager.send_personal_message(
                    response.model_dump_json(), self.__websocket
                )

                self.__logger.info(
                    'Profile complete', session_id=session_id, profile=merged_profile.model_dump()
                )

            elif (
                self.__has_pending_clarifications(merged_confidence)
                and llm_response.followUpQuestion
            ):
                # There are pending clarifications - send follow-up question
                response = Message(
                    event=MessageEvent.ASSISTANT_QUESTION, message=llm_response.followUpQuestion
                )
                await self.__manager.send_personal_message(
                    response.model_dump_json(), self.__websocket, persist=True
                )

            else:
                self.__logger.warning(
                    'No follow-up question provided but profile incomplete',
                    session_id=session_id,
                    profile=merged_profile.model_dump(),
                    confidence=merged_confidence.model_dump(),
                )
                response = Message(
                    event=MessageEvent.ASSISTANT_QUESTION,
                    message='Thank you for the information. Could you please provide any missing details about your wellness profile?',
                )
                await self.__manager.send_personal_message(
                    response.model_dump_json(), self.__websocket
                )

    def __merge_wellness_profile(
        self, existing: WellnessProfile, new: WellnessProfile
    ) -> WellnessProfile:
        """Merge two wellness profiles, with new values taking priority over existing ones."""
        merged_data = existing.model_dump()
        new_data = new.model_dump()

        # Update with new non-null values
        for key, value in new_data.items():
            if value is not None:
                merged_data[key] = value

        return WellnessProfile(**merged_data)

    def __merge_wellness_confidence(
        self, existing: WellnessProfileConfidence, new: WellnessProfileConfidence
    ) -> WellnessProfileConfidence:
        """Merge two confidence profiles, with new values taking priority over existing ones."""
        merged_data = existing.model_dump()
        new_data = new.model_dump()

        # Update with new non-null values
        for key, value in new_data.items():
            if value is not None:
                merged_data[key] = value

        return WellnessProfileConfidence(**merged_data)

    def __has_pending_clarifications(self, confidence: WellnessProfileConfidence) -> bool:
        """Check if there are any fields with low or medium confidence that need clarification."""
        confidence_data = confidence.model_dump()

        for _, conf_level in confidence_data.items():
            if conf_level == Confidence.LOW:
                return True

        return False

    def __is_profile_complete(
        self, profile: WellnessProfile, confidence: WellnessProfileConfidence
    ) -> bool:
        """Check if the wellness profile is complete (all fields filled with high confidence)."""
        profile_data = profile.model_dump()
        confidence_data = confidence.model_dump()

        # Check if all fields are filled and have high confidence
        for field, value in profile_data.items():
            if value is None:
                return False

            conf_level = confidence_data.get(field)
            if conf_level not in (Confidence.HIGH, Confidence.MEDIUM):
                return False

        return True
