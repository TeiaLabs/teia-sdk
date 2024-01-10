from .services.chat_prompts import TemplatingClient
from .services.fcall_completions import FCallCompletionsClient
from .services.text_encodings import TextEncodingClient
from .services.chat_completions import CompletionClient
from .services.tcall_completions import TCallCompletionsClient


class MFClient:
    chat_prompts = TemplatingClient
    completion = CompletionClient
    encoding = TextEncodingClient
    fcall_completion = FCallCompletionsClient
    tcall_completion = TCallCompletionsClient
