import json

from structlog import get_logger

from app.constants.message import MessageEvent, MessageStatus
from app.constants.profiling_stage import ProfilingStage, ProfilingStageMapping
from app.constants.questions import WellnessProfileQuestions
from app.constants.wellness_profile import Confidence
from app.models.message import Message, TransationResponse
from app.models.wellness_profile import WellnessProfile, WellnessProfileConfidence
from app.repositories.shared_state import (
    get_connection_manager,
    session_assistant_replies,
    session_has_pending_generation,
    session_messages,
    session_status,
    session_wellness_confidence,
    session_wellness_profiles,
)
from app.usecases.llm_usecase import LLMUsecase


class WellnessUsecase:
    __slots__ = ('__llm_usecase', '__manager', '__logger')

    def __init__(self):
        self.__llm_usecase = LLMUsecase()
        self.__manager = get_connection_manager()
        self.__logger = get_logger()

    async def initialize_session(self, session_id: str):
        """Initialize the wellness profile session

        :param str session_id: The ID of the session to initialize
        :return TransationResponse: The response from the session initialization
        """
        try:
            connections = self.__manager.get_connections_with_session_id(session_id)
            if not connections:
                return TransationResponse(
                    status=MessageStatus.ERROR, message='No connection found for session'
                )

            response = Message(
                event=MessageEvent.ASSISTANT_QUESTION,
                message=WellnessProfileQuestions.INTRODUCTION,
            )
            await self.__manager.send_message_to_all_connections_with_session_id(
                session_id, response.model_dump_json()
            )

            current_stage = session_status.get(session_id, ProfilingStage.INIT)
            next_stage = ProfilingStageMapping.get_next_stage(current_stage)
            session_status[session_id] = next_stage

            session_wellness_profiles[session_id] = WellnessProfile()
            session_wellness_confidence[session_id] = WellnessProfileConfidence()

        except Exception as e:
            self.__logger.error(f'Error initializing session: {e}')
            response = Message(
                event=MessageEvent.USER_ANSWER,
                message=WellnessProfileQuestions.USER_ANSWER_FAILED,
            )
            await self.__manager.send_message_to_all_connections_with_session_id(
                session_id, response.model_dump_json()
            )

    async def send_message_to_assistant(self, session_id: str, message: Message):
        """Send a message to the assistant

        :param str session_id: The ID of the session to send the message to
        :param Message message: The message to send
        """
        try:
            response = Message(
                event=MessageEvent.USER_ANSWER,
                message=WellnessProfileQuestions.USER_ANSWER_RECEIVED,
            )
            await self.__manager.send_message_to_all_connections_with_session_id(
                session_id, response.model_dump_json(), persist=False
            )

            response_to_save = Message(
                event=MessageEvent.USER_ANSWER,
                message=message.message,
            )
            session_messages[session_id].append(response_to_save.model_dump())

            # Process the user message and handle profile completion
            await self.__process_user_message_and_update_profile(session_id, message.message)

        except Exception as e:
            self.__logger.error(f'Error sending message to user: {e}')
            response = Message(
                event=MessageEvent.USER_ANSWER,
                message=WellnessProfileQuestions.USER_ANSWER_FAILED,
            )
            await self.__manager.send_message_to_all_connections_with_session_id(
                session_id, response.model_dump_json()
            )

    async def __process_user_message_and_update_profile(self, session_id: str, user_message: str):
        """Process user message, update wellness profile, and send appropriate response.

        :param str session_id: The ID of the session
        :param str user_message: The user's message to process
        """
        max_assistant_replies = 5
        if session_assistant_replies.get(session_id, 0) >= max_assistant_replies:
            response = Message(
                event=MessageEvent.MAX_REPLIES_REACHED,
                message='You have hit the max number of replies. Please contact support if you need to continue the conversation.',
            )
            await self.__manager.send_message_to_all_connections_with_session_id(
                session_id, response.model_dump_json()
            )
            return

        if session_has_pending_generation.get(session_id, False):
            response = Message(
                event=MessageEvent.PENDING_GENERATION,
                message='You have pending generation. Please wait for the response.',
            )
            await self.__manager.send_message_to_all_connections_with_session_id(
                session_id, response.model_dump_json()
            )
            return

        # Get LLM response
        session_has_pending_generation[session_id] = True
        llm_response = await self.__llm_usecase.get_output_model_from_user_response(
            user_message,
            WellnessProfileQuestions.INTRODUCTION,
            response_history=session_messages[session_id],
        )
        session_has_pending_generation[session_id] = False

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

        if self.__is_profile_complete(merged_profile, merged_confidence):
            # Profile is complete - send completion message
            response = Message(
                event=MessageEvent.PROFILE_COMPLETE,
                message=json.dumps(merged_profile.model_dump()),
            )
            await self.__manager.send_message_to_all_connections_with_session_id(
                session_id, response.model_dump_json()
            )

            self.__logger.info(
                'Profile complete', session_id=session_id, profile=merged_profile.model_dump()
            )

        elif self.__has_pending_clarifications(merged_confidence) and llm_response.followUpQuestion:
            # There are pending clarifications - send follow-up question
            response = Message(
                event=MessageEvent.ASSISTANT_QUESTION, message=llm_response.followUpQuestion
            )
            await self.__manager.send_message_to_all_connections_with_session_id(
                session_id, response.model_dump_json()
            )

            session_assistant_replies[session_id] = session_assistant_replies.get(session_id, 0) + 1

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
            await self.__manager.send_message_to_all_connections_with_session_id(
                session_id, response.model_dump_json()
            )

    def __merge_wellness_profile(
        self, existing: WellnessProfile, new: WellnessProfile
    ) -> WellnessProfile:
        """Merge two wellness profiles, with new values taking priority over existing ones.

        :param WellnessProfile existing: The existing wellness profile
        :param WellnessProfile new: The new wellness profile
        :return WellnessProfile: The merged wellness profile
        """
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
        """Merge two confidence profiles, with new values taking priority over existing ones.

        :param WellnessProfileConfidence existing: The existing confidence profile
        :param WellnessProfileConfidence new: The new confidence profile
        :return WellnessProfileConfidence: The merged confidence profile
        """
        merged_data = existing.model_dump()
        new_data = new.model_dump()

        # Update with new non-null values
        for key, value in new_data.items():
            if value is not None:
                merged_data[key] = value

        return WellnessProfileConfidence(**merged_data)

    def __has_pending_clarifications(self, confidence: WellnessProfileConfidence) -> bool:
        """Check if there are any fields with low or medium confidence that need clarification.

        :param WellnessProfileConfidence confidence: The confidence profile to check
        :return bool: True if there are any fields with low or medium confidence that need clarification, False otherwise
        """
        confidence_data = confidence.model_dump()

        for _, conf_level in confidence_data.items():
            if conf_level == Confidence.LOW:
                return True

        return False

    def __is_profile_complete(
        self, profile: WellnessProfile, confidence: WellnessProfileConfidence
    ) -> bool:
        """Check if the wellness profile is complete (all fields filled with high confidence).

        :param WellnessProfile profile: The wellness profile to check
        :param WellnessProfileConfidence confidence: The confidence profile to check
        :return bool: True if the wellness profile is complete, False otherwise
        """
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
