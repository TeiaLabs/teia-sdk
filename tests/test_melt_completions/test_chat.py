from melting_schemas.completion.chat import (
    RawChatCompletionRequest,
    ChatCompletionRequest,
    HybridChatCompletionRequest,
    ChatCompletionCreationResponse,
)

from teia_sdk import MFClient


def test_chat_create_one_function_raw():
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
