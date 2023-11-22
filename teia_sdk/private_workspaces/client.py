import logging
import os
from typing import Optional
from urllib.parse import quote


import httpx

from .schemas import (
    PrivateFile,
    PrivateWorkspace,
    PrivateWorkspaceCreationRequest,
    PrivateWorkspaceCreationResponse,
    PrivateWorkspaceIndexing,
)
from ..utils import handle_erros


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
    relative_path = "/workspaces"

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        obj = {
            "Authorization": f"Bearer {TEIA_API_KEY}",
        }
        return obj

    @classmethod
    def replace_file(cls, workspace_id: str, file_path: str):
        with open(file_path, "rb") as f:
            file = f.read()

        res = httpx.put(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/files/",
            headers=cls.get_headers(),
            data=file,
        )
        return res.json()

    @classmethod
    def create_private_workspace(
        cls, workspace: PrivateWorkspaceCreationRequest
    ) -> PrivateWorkspaceCreationResponse:
        """
        Create a private workspace.
        """
        res = httpx.post(
            f"{DATASOURCES_API_URL}{cls.relative_path}/",
            headers=cls.get_headers(),
            json=workspace,
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def get_private_workspaces(
        cls,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        workspace_id: Optional[str] = None,
    ) -> list[PrivateWorkspace]:
        """
        Retrieve a list of private workspaces.
        """
        params = {
            "sort": sort,
            "order": order,
            "limit": limit,
            "offset": offset,
            "workspace_id": workspace_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        res = httpx.get(
            f"{DATASOURCES_API_URL}{cls.relative_path}/",
            headers=cls.get_headers(),
            params=params,
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def get_datasource_files(cls, workspace_id: str) -> PrivateWorkspace:
        """
        Get a private workspace.
        """
        res = httpx.get(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/",
            headers=cls.get_headers(),
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def list_file(
        cls, workspace_id: str, file_path: str, return_content: Optional[bool] = None
    ) -> PrivateFile:
        """
        Show a specific file in a given private workspace.
        """
        res = httpx.get(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/{file_path}/",
            headers=cls.get_headers(),
            params={"return_content": return_content},
        )
        handle_erros(res)
        return res.json()

    # TODO: filepath is redirecting the url - how can we fix this?
    @classmethod
    def upload_file(cls, workspace_id: str, file_path: str) -> PrivateFile:
        """
        Uploads a file to be processed.
        """
        with open(file_path, "rb") as f:
            file = f.read()
        encoded_file_path = quote(file_path)
        print(encoded_file_path)

        print(file)

        res = httpx.post(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/{encoded_file_path}/",
            headers=cls.get_headers(),
            data=file,
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def list_files(
        cls,
        workspace_id: str,
        file_path: Optional[str] = None,
        file_name: Optional[str] = None,
        file_type: Optional[str] = None,
        return_file_content: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ) -> list[PrivateFile]:
        """
        Shows files in a given private workspace.
        """
        params = {
            "file_path": file_path,
            "file_name": file_name,
            "file_type": file_type,
            "return_file_content": return_file_content,
            "limit": limit,
            "offset": offset,
            "sort": sort,
            "order": order,
        }
        params = {k: v for k, v in params.items() if v is not None}
        res = httpx.get(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/files/",
            headers=cls.get_headers(),
            params=params,
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def get_indexings(
        cls,
        workspace_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ) -> list[PrivateWorkspaceIndexing]:
        """
        Get information from all indexing processes in a workspace.
        """
        params = {
            "limit": limit,
            "offset": offset,
            "sort": sort,
            "order": order,
        }
        params = {k: v for k, v in params.items() if v is not None}
        res = httpx.get(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/indexings/",
            headers=cls.get_headers(),
            params=params,
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def create_indexing(cls, workspace_id: str) -> PrivateWorkspaceIndexing:
        """
        Uploads a file to be processed.
        """
        res = httpx.post(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/indexings/",
            headers=cls.get_headers(),
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def get_indexing(
        cls,
        workspace_id: str,
        indexing_id: str,
    ) -> PrivateWorkspaceIndexing:
        """
        Get information from an indexing process.
        """
        res = httpx.get(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/indexings/{indexing_id}/",
            headers=cls.get_headers(),
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def delete_private_workspace(cls, workspace_id: str):
        """
        Delete workspace and all resources related to it.
        """
        res = httpx.delete(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/",
            headers=cls.get_headers(),
        )
        handle_erros(res)
        return res

    @classmethod
    def search_workspace(
        cls,
        workspace_id: str,
        query: str,
        num_results: Optional[int] = None,
        schemaless: Optional[bool] = None,
    ) -> list[dict]:
        """
        Perform an embedding search in a private workspace.
        """
        params = {
            "query": query,
            "num_results": num_results,
            "schemaless": schemaless,
        }
        params = {k: v for k, v in params.items() if v is not None}
        res = httpx.get(
            f"{DATASOURCES_API_URL}{cls.relative_path}/{workspace_id}/search/",
            headers=cls.get_headers(),
            params=params,
        )
        handle_erros(res)
        return res.json()
