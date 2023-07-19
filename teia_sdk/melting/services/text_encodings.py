import httpx
from melting_schemas.encoding.text_encoding import RawTextEncoding, TextEncodingResponse

from .. import TEIA_API_KEY, MELT_API_URL
from ...utils import handle_erros


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
