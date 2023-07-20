import httpx
from melting_schemas.completion.fcall import RawFCallRequest, FCallCompletionCreationResponse

from .. import TEIA_API_KEY, MELT_API_URL
from ...utils import handle_erros


class FCallCompletionsClient:
    relative_path = "/text-generation/fcall-completions"

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        obj = {
            "Authorization": f"Bearer {TEIA_API_KEY}",
        }
        return obj

    @classmethod
    def create_one(cls, body: RawFCallRequest) -> FCallCompletionCreationResponse:
        res = httpx.post(
            f"{MELT_API_URL}{cls.relative_path}/create",
            headers=cls.get_headers(),
            json=body.dict(),
        )
        handle_erros(res)
        return res.json()
