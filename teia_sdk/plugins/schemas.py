from typing import Optional, TypedDict


class PluginInfo(TypedDict):
    name: str
    method: str
    params: dict
    response: str | dict
    error: str
    response_time: int


class PluginResponse(TypedDict):
    selector_completion: str
    plugin_selection_id: str
    plugin_execution_id: str
    plugins_infos: Optional[list[PluginInfo] | None]
    error: str


class SelectPlugin(TypedDict):
    prompt_name: str
    current_message: str
    context: str
    plugin_names: list[str]


class PluginUsage(TypedDict):
    plugin: str
    method: str
    arguments: dict
