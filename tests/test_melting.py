from melting_schemas.completion.fcall import RawFCallRequest, FCallCompletionCreationResponse
from pydantic import create_model_from_typeddict
from teia_sdk import MFClient


def test_fcall_create_one():
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
    pydantic_model = create_model_from_typeddict(FCallCompletionCreationResponse)
