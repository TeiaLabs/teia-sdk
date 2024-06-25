import json
from typing import Iterator, Optional

import httpx
import requests
from melting_schemas.completion.tcall import (
    ChatChunk,
    TCallCompletionCreationResponse,
    TCallRequest,
    ToolCallChunk,
    ToolCallMLMessage,
)
from melting_schemas.utils import UsageInfo

from ...exceptions import TeiaSdkError
from ...utils import handle_erros
from .. import MELT_API_URL, TEIA_API_KEY

STREAM_MESSAGE = ToolCallMLMessage | ToolCallChunk | ChatChunk | UsageInfo


class TCallCompletionsClient:
    relative_path = "/text-generation/tcall-completions"
    client = httpx.Client(timeout=60)

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        obj = {
            "Authorization": f"Bearer {TEIA_API_KEY}",
        }
        return obj

    @classmethod
    def create_one(
        cls, body: TCallRequest, user_email: Optional[str] = None
    ) -> TCallCompletionCreationResponse:
        headers = cls.get_headers()
        if user_email:
            headers["X-User-Email"] = user_email

        res = cls.client.post(
            f"{MELT_API_URL}{cls.relative_path}/create",
            headers=headers,
            json=body.dict(),
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def stream_one(
        cls,
        body: TCallRequest,
        count_tokens: bool = False,
        user_email: Optional[str] = None,
    ) -> tuple[str, Iterator[STREAM_MESSAGE]]:
        if not isinstance(body, dict):
            body = body.dict(exclude_none=True)

        headers = cls.get_headers()
        if count_tokens:
            headers["X-Count-Tokens"] = "true"
        if user_email:
            headers["X-User-Email"] = user_email

        res = requests.post(
            url=f"{MELT_API_URL}{cls.relative_path}/stream",
            headers=headers,
            json=body,
            stream=True,
        )
        try:
            res.raise_for_status()
        except requests.HTTPError as e:
            raise TeiaSdkError(res.json()) from e
        identifier = res.headers["Content-Location"].split("/")[-1]
        return identifier, map(json.loads, res.iter_lines())
