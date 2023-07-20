from melting_schemas.completion.fcall import RawFCallRequest, FCallCompletionCreationResponse
from teia_sdk import MFClient


def test_fcall_create_one_function_augmented_completion():
    body = RawFCallRequest(
        functions=[
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                },
            }
        ],
        messages=[
            {
                "role": "user",
                "content": "What is the weather like in Boston?",
            },
            {
                "role": "assistant",
                "content": None,
                "function_call": {
                    "name": "get_current_weather",
                    "arguments": '{"location": "Boston, MA"}',
                },
            },
            {
                "role": "function",
                "name": "get_current_weather",
                "content": '{"temperature": "22", "unit": "celsius", "description": "Sunny"}',
            },
        ],
        settings={"model": "gpt-3.5-turbo-0613"},
    )
    res = MFClient.fcall_completion.create_one(body)
    FCallCompletionCreationResponse(**res)
    assert "22" in res["output"]["content"]


def test_fcall_create_one_function_call():
    body = RawFCallRequest(
        functions=[
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                },
            }
        ],
        messages=[
            {
                "role": "user",
                "content": "What is the weather like in Boston?",
            },
        ],
        settings={"model": "gpt-3.5-turbo-0613"},
    )
    res = MFClient.fcall_completion.create_one(body)
    FCallCompletionCreationResponse(**res)
    assert res["output"]["content"] is None
    assert res["output"]["function_call"]["name"] == "get_current_weather"
    assert "Boston" in res["output"]["function_call"]["arguments"]
