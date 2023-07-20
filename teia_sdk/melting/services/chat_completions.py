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
    def create_one(cls, body: dict) -> ChatCompletionCreationResponse:
        res = httpx.post(
            f"{MELT_API_URL}{cls.relative_path}/create",
            headers=cls.get_headers(),
            json=body,
        )
        handle_erros(res)
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
        cls, body: dict
    ) -> tuple[str, Iterator[StreamedChatCompletionCreationResponse]]:
        with httpx.stream(
            "POST", f"{MELT_API_URL}{cls.relative_path}/stream", headers=cls.get_headers(), json=body
        ) as res:
            identifier = res.headers["Content-Location"].split("/")[-1]
            return identifier, map(json.loads, res.iter_lines())
