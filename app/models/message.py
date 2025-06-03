from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.constants.message import MessageEvent, MessageStatus


class Message(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra='forbid')

    event: MessageEvent
    status: Optional[MessageStatus] = None
    message: Optional[str] = None


class TransationResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra='forbid')

    status: MessageStatus
    message: Optional[str] = None


class UserAnswerInput(BaseModel):
    model_config = ConfigDict(extra='forbid')

    message: Annotated[str, StringConstraints(min_length=1, max_length=1000)] = Field(
        description='The message to send to the Assistant'
    )
