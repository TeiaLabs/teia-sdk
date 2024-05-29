import os
from typing import Literal, Optional

import httpx
from starlette import status as s

from .schemas import Connection


class DbsailorClient:

    def __init__(
        self,
        user_email: str,
        api_key: Optional[str] = os.getenv("TEIA_API_KEY", None),
        url: str = os.getenv(
            "DBSAILOR_URL",
            "https://dbsailor.allai.digital",
        ),
    ):
        if api_key is None:
            m = "'TEIA_API_KEY' env var is required or api_key param must be informed."
            raise ValueError(m)
        self.api_key = api_key
        self.url = url

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "x-user-email": user_email,
        }

        self.http_client = httpx.Client(
            base_url=self.url,
            headers=self.headers,
        )

    @classmethod
    def handle_errors(cls, response):
        if response.status_code == s.HTTP_409_CONFLICT:
            raise Exception(response.json()["detail"])
        if response.status_code == s.HTTP_404_NOT_FOUND:
            raise Exception(response.json()["detail"])

    def create_connection(self, connection: Connection):
        connection_json = connection.model_dump()
        res = self.http_client.post("/connections", json=connection_json)
        self.handle_errors(res)
        res.raise_for_status()
        return res.json()

    def read_many_connections(
        self,
        name_startswith: Optional[str],
        type: Optional[Literal["atlas", "milvus"]],
        service_name: Optional[str],
        entity_name: Optional[str],
        sort: Optional[str] = "created_at",
        order: Optional[str] = "desc",
        offset: Optional[int] = 0,
        limit: Optional[int] = 1024,
    ):

        params = {
            "name_startswith": name_startswith,
            "type": type,
            "service_name": service_name,
            "entity_name": entity_name,
            "$sort": sort,
            "$order": order,
            "$offset": offset,
            "$limit": limit,
        }

        res = self.http_client.get("/connections", params=params)
        self.handle_errors(res)
        res.raise_for_status()
        return [Connection(**x) for x in res.json()]

    def read_connection(self, name: str):
        res = self.http_client.get(f"/connections{name}")
        self.handle_errors(res)
        res.raise_for_status()
        return Connection(**res.json())

    def delete_connection(self, name: str):
        res = self.http_client.delete(f"/connections{name}")
        self.handle_errors(res)
        res.raise_for_status()
        return res.json()
