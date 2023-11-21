import logging
import os

import httpx

from private_workspaces.schemas import (
    PrivateWorkspaceCreationRequest,
    PrivateWorkspaceCreationResponse,
)


logger = logging.getLogger(__name__)

try:
    TEIA_API_KEY = os.environ["TEIA_API_KEY"]
    DATASOURCES_API_URL = os.getenv(
        "DATASOURCES_API_URL", "https://datasources.teialabs.com.br"
    )
except KeyError:
    m = "[red]MissingEnvironmentVariables[/red]: "
    m += "[yellow]'TEIA_API_KEY'[/yellow] cannot be empty."
    print(m)
    exit(1)


class PrivateWorkspaceClient:
    client = httpx.Client(timeout=60)
    relative_path = "/api/workspaces"

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        obj = {
            "Authorization": f"Bearer {TEIA_API_KEY}",
        }
        return obj

    @classmethod
    def create_private_workspace(
        cls, workspace: PrivateWorkspaceCreationRequest
    ) -> PrivateWorkspaceCreationResponse:
        res = cls.client.post(
            f"{cls.relative_path}/{DATASOURCES_API_URL}/",
            headers=cls.get_headers(),
            json=workspace,
        )
        return res
