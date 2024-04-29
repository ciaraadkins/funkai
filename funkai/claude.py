from .manager import FunkManager

class ClaudeFunk(FunkManager):
    provider = 'claude'
    
    def __init__(self, api_key, model="claude-3-opus-20240229"):
        super().__init__(api_key, model)