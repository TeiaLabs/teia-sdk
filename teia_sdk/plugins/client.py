import os
import httpx
from starlette import status as http_status

from . import exceptions
from .schemas import PluginResponse, SelectPlugin, PluginUsage, PluginInfo


try:
    TEIA_API_KEY = os.environ["TEIA_API_KEY"]
    PLUGINS_API_URL = os.getenv("PLUGINS_API_URL", "https://athena.teialabs.com.br:3333")
except KeyError:
    m = "[red]MissingEnvironmentVariables[/red]: "
    m += "[yellow]'TEIA_API_KEY'[/yellow] cannot be empty."
    print(m)
    exit(1)


class PluginClient:
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
        return res.json()

    @classmethod
    def select_and_run_plugin(
        cls,
        prompt_name: str,
        current_message: str,
        context: str,
        plugin_names: list[str]
    ) -> PluginResponse:

        if not plugin_names:
            return PluginResponse(
                selector_completion="",
                plugins_infos=[],
                error=f"No plugins in plugin_names"
            )

        sp = SelectPlugin(
            prompt_name=prompt_name,
            current_message=current_message,
            context=context,
            plugin_names=plugin_names,
        )

        sel_run_url = f"{PLUGINS_API_URL}/select-and-run-plugin"
        plugins_data = httpx.post(
            sel_run_url,
            json=sp,
            headers=cls.get_headers(),
        )
        if plugins_data.status_code != http_status.HTTP_200_OK:
            raise exceptions.ErrorPluginAPISelectAndRun(
                f"Request: {sel_run_url}\njson: {sp}\nError: {plugins_data.status_code}: {plugins_data.text}. "
            )

        try:
            plugins_data = plugins_data.json()
        except AttributeError:
            raise exceptions.ErrorToGetPluginResponse(
                f"Tried to convert response to json. Response: {plugins_data}. "
            )

        plugins_data["plugins_infos"] = [
            PluginInfo(**p) for p in plugins_data["plugins_infos"]
        ]
        plugins_data = PluginResponse(**plugins_data)

        return plugins_data

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
