from .manager import FunkManager

class OpenAIFunk(FunkManager):
    provider = 'openai'
    
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        super().__init__(api_key, model)