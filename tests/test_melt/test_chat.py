import pytest

from melting_schemas.completion.chat import (
    RawChatCompletionRequest,
    ChatCompletionRequest,
    HybridChatCompletionRequest,
    ChatCompletionCreationResponse,
)

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


class TestMFChatCompletions:
    def test_create_one(self):
        body = RawChatCompletionRequest(
            messages=[
                {
                    "role": "user",
                    "content": "What is 10+10?",
                },
            ],
            settings={"model": "gpt-3.5-turbo"},
        )
        res = MFClient.completion.create_one(body.dict())
        ChatCompletionCreationResponse(**res)
        assert "20" in res["output"]["content"]

    def test_create_one_prompted(self, insert_prompt):
        body = ChatCompletionRequest(
            prompt_inputs=[
                {
                    "role": "user",
                    "inputs": {"question": "What is the secret number?"},
                    "template_name": "user_prompt",
                },
            ],
            prompt_name="test.prompt.teia_sdk",
        )
        response = MFClient.completion.create_one(body=body.dict())
        ChatCompletionCreationResponse(**response)
        assert "Yo" in response["output"]["content"]

    def test_stream_one(self):
        body = RawChatCompletionRequest(
            messages=[
                {
                    "role": "user",
                    "content": "What is 10+10?",
                },
            ],
            settings={"model": "gpt-3.5-turbo"},
        )
        id, res = MFClient.completion.stream_one(body.dict())
        assert len(list(res)) > 0

    def test_read_one(self):
        pass
