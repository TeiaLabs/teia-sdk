from typing import Optional, TypedDict
from melting_schemas.completion.fcall import ChatMLMessage, FCallModelSettings


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
    messages: list[ChatMLMessage]
    plugin_names: list[str]
    model_settings: FCallModelSettings
    plugin_extra_arguments: dict[str, dict]


class PluginUsage(TypedDict):
    plugin: str
    method: str
    arguments: dict


class PluginCall(TypedDict):
    plugin: str
    method: str
    arguments: dict


class GetPluginSelection(TypedDict):
    plugin_selector: SelectPlugin
    plugin_usage: list[PluginCall]
    completion_id: str
    error: str


class GetPluginExecution(TypedDict):
    plugin_calls: list[PluginCall]
    plugin_infos: list[PluginInfo]
    error: str
