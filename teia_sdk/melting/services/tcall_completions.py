import httpx
from typing import Optional
from melting_schemas.completion.tcall import (
    TCallRequest,
    TCallCompletionCreationResponse,
)

from .. import TEIA_API_KEY, MELT_API_URL
from ...utils import handle_erros


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
        if not isinstance(body, dict):
            body = body.dict(exclude_none=True)

        headers = cls.get_headers()
        if user_email:
            headers["X-User-Email"] = user_email

        res = cls.client.post(
            f"{MELT_API_URL}{cls.relative_path}/create",
            headers=headers,
            json=body,
        )
        handle_erros(res)
        return res.json()
