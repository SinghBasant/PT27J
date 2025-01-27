from .gemini_helper import GeminiProvider
from .openai_helper import OpenAIProvider

class AIFactory:
    @staticmethod
    def get_provider(provider_name: str):
        providers = {
            "Gemini": GeminiProvider,
            "OpenAI": OpenAIProvider
        }
        
        provider_class = providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        return provider_class()