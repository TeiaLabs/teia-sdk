from datetime import datetime
from typing import Optional, TypedDict

from melting_schemas.enginius import ChatMLMessage
from melting_schemas.historian import Templating

from melting_face.completion.types import FinishReason, TokenUsage
from tauth.schemas import Creator


class ChatCompletionResponse(TypedDict):
    _id: str
    created_at: datetime
    created_by: Creator
    finish_reason: FinishReason
    messages: list[ChatMLMessage]
    output: ChatMLMessage
    settings: dict
    templating: Optional[Templating]
    timings: dict
    usage: TokenUsage
