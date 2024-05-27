import os
from typing import Optional

import httpx
from dbsailor_schemas.connection import Connection
from starlette import status as s


class DbsailorClient:

    def __init__(
        self,
        user_email: str,
        api_key: Optional[str] = os.getenv("TEIA_API_KEY", None),
        url: str = os.getenv(
            "DBSAILOR_URL",
            "https://dbsailor-api-prod-alb-1466075297.us-east-1.elb.amazonaws.com",
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

    def read_many_connections(self):
        res = self.http_client.get("/connections")
        self.handle_errors(res)
        res.raise_for_status()
        return res.json()

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
