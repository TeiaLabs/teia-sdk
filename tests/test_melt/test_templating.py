import pytest

from melting_schemas.templating.prompt import ChatPromptTemplate

from teia_sdk import MFClient


@pytest.fixture()
def insert_prompt():
    MFClient.chat_prompts.post(
        body={
            "name": "test.prompt.teia_sdk",
            "description": "A promtp for testing the teia_sdk.",
            "settings": {
                "model": "gpt-3.5-turbo",
                "max_tokens": 200,
                "temperature": 0.25,
            },
            "system_templates": "You are a AI bot that allways starts your messages with Yo!.",
            "user_templates": [
                {"template_name": "user_prompt", "template": "<question>"}
            ],
            "assistant_templates": [
                {"template_name": "assistant_prompt", "template": "<message>"}
            ],
        }
    )
    yield
    MFClient.chat_prompts.delete(name="test.prompt.teia_sdk")


class TestMFClientTemplating:
    def test_post(self):
        body = {
            "name": "teia_sdk.prompt_test.post",
            "description": "A development example.",
            "settings": {
                "model": "gpt-3.5-turbo",
                "max_tokens": 200,
                "temperature": 0.25,
            },
            "system_templates": [
                {"template_name": "plugin_prompt", "template": "<plugin_data>"}
            ],
            "user_templates": [
                {"template_name": "user_prompt", "template": "<question>"}
            ],
            "assistant_templates": [
                {"template_name": "assistant_prompt", "template": "<message>"}
            ],
        }
        MFClient.chat_prompts.post(body=body)
        response = MFClient.chat_prompts.read_one(name="teia_sdk.prompt_test.post")
        print(response)
        response = response[0]
        assert response["name"] == "teia_sdk.prompt_test.post"
        assert response["description"] == "A development example."
        MFClient.chat_prompts.delete(name="teia_sdk.prompt_test.post")

    def test_read_one(self, insert_prompt):
        response = MFClient.chat_prompts.read_one(name="test.prompt.teia_sdk")
        response = response[0]
        assert response["name"] == "test.prompt.teia_sdk"
        assert response["description"] == "A promtp for testing the teia_sdk."
        assert response["settings"]["model"] == "gpt-3.5-turbo"

    def test_read_many(self):
        pass

    def test_deletion(self):
        pass
