import pytest
from teia_sdk import PluginClient
from teia_sdk.utils import ppjson


class TestPluginsClient:
    @pytest.fixture
    def client(self):
        return PluginClient()

    def test_aveilable(self, client: PluginClient):
        assert len(client.available_plugins().keys()) == 3

    def test_select_and_run_plugin(self, client: PluginClient):
        response = client.select_and_run_plugin(
            prompt_name="teia.plugins-api.plugin-selector",
            current_message=" whats the waetther like in New York right now?",
            context="test",
            plugin_names=["weather_plugin"],
        )
        assert response["plugin_infos"][0]["params"]["place"] == "New York"
        assert response["plugin_infos"][0]["name"] == "weather_plugin"

    def test_select_plugin(self, client: PluginClient):
        response = client.run_selector(
            prompt_name="teia.plugins-api.plugin-selector",
            current_message="whats the waetther like in New York right now?",
            context="test",
            plugin_names=["weather_plugin"],
        )
        print(ppjson(response))
        assert response["arguments"]["place"] == "New York"
        assert response["plugin"] == "weather_plugin"

    def test_run_plugin(self, client: PluginClient):
        plugin_calls = [
            {
                "plugin": "weather_plugin",
                "method": "current",
                "arguments": {"place": "New York"},
            }
        ]
        response = client.run_plugins(plugin_calls=plugin_calls)
        assert response["plugin_infos"][0]["params"]["place"] == "New York"
        assert response["plugin_infos"][0]["name"] == "weather_plugin"
