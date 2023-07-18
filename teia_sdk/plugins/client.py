import os
import httpx
from pydantic import BaseModel
from typing import Optional, TypedDict
from .schemas import PluginResponse, SelectPlugin, PluginUsage
from ..utils import handle_erros


try:
    TEIA_API_KEY = os.environ["TEIA_API_KEY"]
    PLUGINS_API_URL = os.getenv("PLUGINS_API_URL", "http://54.81.193.45:5000/")
except KeyError:
    m = "[red]MissingEnvironmentVariables[/red]: "
    m += "[yellow]'TEIA_API_KEY'[/yellow] cannot be empty."
    print(m)
    exit(1)


class PluginSelectorClient:
    @classmethod
    def get_headers(cls) -> dict[str, str]:
        obj = {
            "Authorization": f"Bearer {TEIA_API_KEY}",
        }
        return obj

    @classmethod
    def available_plugins(cls) -> dict[str, dict]:
        res = httpx.get(
            f"{PLUGINS_API_URL}/available",
            headers=cls.get_headers(),
        )
        handle_erros(res)
        return res.json()

    @classmethod
    def run_selector(
        cls, message: str, context: str, plugin_list: list[str], prompt_name: str
    ):
        sp = SelectPlugin(
            prompt_name=prompt_name,
            current_message=message,
            context=context,
            plugin_names=plugin_list,
        )

        plugin_host = PLUGINS_API_URL
        headers = cls.get_headers()
        plugins_selected = httpx.post(
            f"{plugin_host}/select-plugin",
            data=sp.json(),
            headers=headers,
        )

        print(plugins_selected)
        print(plugins_selected.status_code)
        print(plugins_selected.text)

        from starlette import status as http_status

        if plugins_selected.status_code != http_status.HTTP_200_OK:
            return PluginResponse(
                selector_completion="",
                plugins_infos=[],
                error=f"{plugins_selected.status_code}: {plugins_selected.text}",
            )

        print("plugins_selected", plugins_selected)

        plugin_calls = PluginUsage(**plugins_selected.json()["plugin_usage"][0])

        plugin_payload = str([plugin_calls.dict()])

        body_data = {
            "plugin_selector_payload": plugin_payload,
        }

        plugin_data = httpx.post(
            f"{plugin_host}/run-plugin",
            params=body_data,
            headers=headers,
        )

        print(plugin_data)

        if plugins_selected.status_code != http_status.HTTP_200_OK:
            plugin_data = PluginResponse(
                selector_completion=plugins_selected,
                error=f"{plugin_data.status_code}: {plugin_data.text}",
            )
            return plugin_data

        plugin_data = plugin_data.json()
        plugin_data = PluginResponse(**plugin_data)

        return plugin_data
