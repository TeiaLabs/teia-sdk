import datetime
from typing import NotRequired, TypedDict

from tauth.schemas import Creator


class IndexingSettings(TypedDict):
    model: str
    parsers: NotRequired[dict[str, str]]


class PrivateWorkspaceCreationRequest(TypedDict):
    name: str
    indexing_settings: IndexingSettings


class PrivateWorkspaceCreationResponse(PrivateWorkspaceCreationRequest):
    created_at: datetime
    created_by: Creator
    workspace_id: str
