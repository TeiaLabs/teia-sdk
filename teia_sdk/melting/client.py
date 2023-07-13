import json
import os
from typing import Any, Iterator, Optional

import httpx
import requests
from rich import print
from melting_schemas.historian.chat_completions import (
    ChatCompletionCreationResponse,
    StreamedChatCompletionCreationResponse,
)
from melting_schemas.templating import ChatPromptTemplate
from melting_schemas.templating.prompt import ChatPrompt, GeneratedFields
from melting_schemas.encoding.text_encoding import RawTextEncoding, TextEncodingResponse

from .schemas import ChatCompletionResponse
from ..utils import handle_erros

try:
    TEIA_API_KEY = os.environ["TEIA_API_KEY"]
    MELT_API_URL = os.getenv("MELT_API_URL", "https://meltingface.teialabs.com.br/api")
except KeyError:
    m = "[red]MissingEnvironmentVariables[/red]: "
    m += "[yellow]'TEIA_API_KEY'[/yellow] cannot be empty."
    print(m)
    exit(1)


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
        res = requests.post(
            f"{MELT_API_URL}{cls.relative_path}/stream",
            headers=cls.get_headers(),
            json=body,
            stream=True,
        )
        # TODO: use httpx instead of requests
        identifier = res.headers["Content-Location"].split("/")[-1]
        return identifier, map(json.loads, res.iter_lines())


class TemplatingClient:
    relative_path = "/templating/chat-prompts"

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        obj = {
            "Authorization": f"Bearer {TEIA_API_KEY}",
        }
        return obj

    @classmethod
    def read_one(cls, identifier: Optional[str], name: Optional[str]) -> ChatPrompt:
        if identifier is not None:
            res = httpx.get(
                f"{MELT_API_URL}{cls.relative_path}/{identifier}",
                headers=cls.get_headers(),
            )
        elif name is not None:
            res = httpx.get(
                f"{MELT_API_URL}{cls.relative_path}",
                headers=cls.get_headers(),
                params={"name": name},
            )
        else:
            raise ValueError("Must provide either 'identifier' or 'name'.")
        handle_erros(res)
        return res.json()

    @classmethod
    def read_many(
        cls, name: Optional[str], model: Optional[str], limit: int, skip: int
    ) -> list[ChatPrompt]:
        params = {"name": name, "settings.model": model, "$limit": limit, "$skip": skip}
        params = {k: v for k, v in params.items() if v is not None}
        res = httpx.get(
            f"{MELT_API_URL}{cls.relative_path}",
            headers=cls.get_headers(),
            params=params,
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def post(cls, body: ChatPromptTemplate) -> GeneratedFields:
        res = httpx.post(
            f"{MELT_API_URL}{cls.relative_path}",
            headers=cls.get_headers(),
            json=body,
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def delete(cls, name: str) -> dict[str, Any]:
        res = httpx.delete(
            f"{MELT_API_URL}{cls.relative_path}/{name}",
            headers=cls.get_headers(),
        )
        try:
            res.raise_for_status()
            return {"status_code": res.status_code}
        except httpx.HTTPError:
            body = res.json()
            return {"status_code": res.status_code, **body}


class TextEncodingClient:
    relative_path = "/text-encodings"

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        obj = {
            "Authorization": f"Bearer {TEIA_API_KEY}",
        }
        return obj

    @classmethod
    def encode(cls, body: RawTextEncoding) -> TextEncodingResponse:
        res = httpx.post(
            f"{MELT_API_URL}{cls.relative_path}",
            headers=cls.get_headers(),
            json=body,
        )
        handle_erros(res)
        return res.json()


class MFClient:
    chat_prompts = TemplatingClient
    completion = CompletionClient
    encoding = TextEncodingClient
