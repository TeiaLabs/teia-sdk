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
            current_message=" whats the waetther like in new yourk right now?",
            context="test",
            plugin_names=["weather_plugin"],
        )
        ppjson(response)
        assert response["plugin_infos"][0]["params"]["place"] == "New York"
        assert response["plugin_infos"][0]["name"] == "weather_plugin"

    def test_select_plugin(self, client: PluginClient):
        pass

    def test_run_plugin():
        pass
