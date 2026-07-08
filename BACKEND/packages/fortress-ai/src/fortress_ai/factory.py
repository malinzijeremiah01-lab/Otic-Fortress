import os
from .mock_provider import MockModelProvider


def create_model_provider():
    provider = os.getenv("MODEL_PROVIDER", "mock")
    if provider == "mock":
        return MockModelProvider()
    if provider == "azure_openai":
        from .azure_openai_provider import AzureOpenAIProvider
        return AzureOpenAIProvider()
    if provider == "huggingface":
        from .huggingface_provider import HuggingFaceProvider
        return HuggingFaceProvider()
    if provider == "grok":
        from .external.grok_provider import GrokProvider
        return GrokProvider()
    raise ValueError(f"Unsupported MODEL_PROVIDER={provider}")
