from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.constants.message import MessageEvent


class Message(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra='forbid')

    event: MessageEvent
    message: Optional[str] = None
