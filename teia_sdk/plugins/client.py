import os
import httpx
import logging
from typing import Optional
from starlette import status as http_status

from . import exceptions
from .schemas import (
    PluginResponse,
    SelectPlugin,
    PluginUsage,
    PluginInfo,
)
from melting_schemas.completion.fcall import ChatMLMessage, FCallModelSettings


logger = logging.getLogger(__name__)

try:
    TEIA_API_KEY = os.environ["TEIA_API_KEY"]
    PLUGINS_API_URL = os.getenv(
        "PLUGINS_API_URL", "https://plugins.athena.teialabs.com.br"
    )
except KeyError:
    m = "[red]MissingEnvironmentVariables[/red]: "
    m += "[yellow]'TEIA_API_KEY'[/yellow] cannot be empty."
    print(m)
    exit(1)


class PluginClient:
    client = httpx.Client(timeout=60)

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
        messages: list[ChatMLMessage],
        plugin_names: list[str],
        model_settings: FCallModelSettings,
        user_email: Optional[str] = None
    ) -> PluginResponse:
        if not plugin_names:
            return PluginResponse(
                selector_completion="",
                plugin_infos=[],
                error=f"No plugins in plugin_names",
            )

        sp = SelectPlugin(
            messages=messages,
            plugin_names=plugin_names,
            model_settings=model_settings
        )

        sel_run_url = f"{PLUGINS_API_URL}/select-and-run-plugin"
        headers = cls.get_headers()
        if user_email:
            headers["X-User-Email"] = user_email

        logger.debug(f"Requesting {sel_run_url}. Args: {sp}. Headers: {headers}.")
        try:
            plugins_data = cls.client.post(
                sel_run_url,
                json=sp,
                headers=headers
            )
            logger.debug(f"Request returned: {plugins_data}, {plugins_data.status_code}.")
        except httpx.ReadTimeout as ex:
            raise exceptions.ErrorPluginAPISelectAndRun(
                f"Request to {sel_run_url} timed out\nError: {ex}. "
            )
        except Exception as ex:
            raise exceptions.ErrorPluginAPISelectAndRun(
                f"Request to {sel_run_url} did not work\nError: {ex}. "
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

        plugins_data["plugin_infos"] = [
            PluginInfo(**p) for p in plugins_data["plugin_infos"]
        ]
        plugins_data = PluginResponse(**plugins_data)

        return plugins_data

    @classmethod
    def run_selector(
        cls,
        messages: list[ChatMLMessage],
        plugin_names: list[str],
        model_settings: FCallModelSettings,
    ) -> PluginUsage:
        sp = SelectPlugin(
            messages=messages,
            plugin_names=plugin_names,
            model_settings=model_settings,
        )

        plugins_selected = cls.client.post(
            f"{PLUGINS_API_URL}/select-plugin",
            json=sp,  # errado
            headers=cls.get_headers(),
        )

        plugins_selected.raise_for_status()
        print("plugins_selected", plugins_selected)

        plugin_calls = PluginUsage(**plugins_selected.json()["plugin_usage"][0])
        return plugin_calls

    @classmethod
    def run_plugins(cls, plugin_calls: list[PluginUsage]):
        plugin_data = httpx.post(
            f"{PLUGINS_API_URL}/run-plugin",
            json=plugin_calls,
            headers=cls.get_headers(),
        )

        plugin_data.raise_for_status()

        plugin_data = plugin_data.json()
        plugin_data = PluginResponse(**plugin_data)

        return plugin_data
