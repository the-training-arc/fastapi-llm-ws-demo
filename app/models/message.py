from typing import Optional

from pydantic import BaseModel, ConfigDict

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
