import json
import os
from typing import Any, Iterator, Optional

import httpx
import requests
from melting_schemas.historian.chat_completions import (
    ChatCompletionCreationResponse,
    StreamedChatCompletionCreationResponse,
)

from ...utils import handle_erros
from .. import MELT_API_URL, TEIA_API_KEY
from ..schemas import ChatCompletionResponse


class CompletionClient:
    relative_path = "/historian/chat-completions"

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        obj = {
            "Authorization": f"Bearer {TEIA_API_KEY}",
        }
        return obj

    @classmethod
    def create_one(
        cls, body: dict, user_email: Optional[str] = None
    ) -> ChatCompletionCreationResponse:
        headers = cls.get_headers()
        if user_email:
            headers["X-User-Email"] = user_email

        res = httpx.post(
            f"{MELT_API_URL}{cls.relative_path}/create",
            timeout=15,
            headers=headers,
            json=body,
        )

        return res.json()

    @classmethod
    def read_one(cls, identifier: str) -> ChatCompletionResponse:
        res = httpx.get(
            f"{MELT_API_URL}{cls.relative_path}/{identifier}",
            headers=cls.get_headers(),
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def stream_one(
        cls,
        body: dict,
        count_tokens: bool = False,
        user_email: Optional[str] = None,
    ) -> tuple[str, Iterator[StreamedChatCompletionCreationResponse]]:
        headers = cls.get_headers()
        if count_tokens:
            headers["X-Count-Tokens"] = "true"
        if user_email:
            headers["X-User-Email"] = user_email

        res = requests.post(
            f"{MELT_API_URL}{cls.relative_path}/stream",
            headers=headers,
            json=body,
            stream=True,
        )
        # TODO: use httpx stream instead of requests
        identifier = res.headers["Content-Location"].split("/")[-1]
        return identifier, map(json.loads, res.iter_lines())
