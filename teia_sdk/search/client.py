import os
import httpx

try:
    SEARCH_API_KEY = os.environ["SEARCH_API_KEY"]
    SEARCH_API_URL = os.getenv("SEARCH_API_URL", "https://athena.teialabs.com.br:3232")
except KeyError:
    m = "[red]MissingEnvironmentVariables[/red]: "
    m += "[yellow]'SEARCH_API_KEY'[/yellow] cannot be empty."
    print(m)
    exit(1)


class SearchClient:
    relativepath = "/search"

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        obj = {
            "Authorization": f"Bearer {SEARCH_API_KEY}",
        }
        return obj

    @classmethod
    def search(cls, query: str) -> dict:
        response = httpx.get(
            url=f"{SEARCH_API_URL}{cls.relativepath}",
            headers=cls.get_headers(),
            params=query,
        )
        return response.json()
