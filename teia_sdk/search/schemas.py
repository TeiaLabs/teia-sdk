from typing import Optional, TypedDict

from tauth.schemas import Creator


class SearchSettings(TypedDict):
    kb_name: str
    threshold: float
    top_k: int


class SearchRequest(TypedDict):
    query: str
    model_name: str
    model_type: str
    search_settings: list[SearchSettings]


class SearchResponse(TypedDict):
    pass
