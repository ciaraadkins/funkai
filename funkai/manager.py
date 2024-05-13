from .funk import Funk

class FunkManager:
    def __init__(self, api_key, default_model):
        self.api_key = api_key
        self.default_model = default_model
        self.funks = {}

    def add(self, name, operation, options, api_key=None, model=None, retry_count=0, input_dtype=str, output_dtype=str):
        api_key = api_key or self.api_key
        model = model or self.default_model

        if name in self.funks:
            raise ValueError(f"A Funk with name '{name}' already exists.")
        
        new_funk = Funk(self.provider, name, operation, api_key, model, options, retry_count, input_dtype, output_dtype)
        if new_funk.error:
            raise ValueError("Invalid Funk Parameters.")
        
        self.funks[name] = new_funk

    def update(self, name, **kwargs):
        funk = self._get(name)
        if not funk:
            raise ValueError(f"No Funk with name '{name}' found.")
        
        for key, value in kwargs.items():
            if hasattr(funk, key):
                setattr(funk, key, value)
            else:
                raise ValueError(f"Invalid parameter '{key}' for Funk instance.")

        self.funks[name] = funk
        
    def _get(self, name):
        return self.funks.get(name)

    def remove(self, name):
        self.funks.pop(name, None)

    def run(self, name, input_content, examples=None, full_resp=False):
        funk = self._get(name)
        
        if not funk:
            raise ValueError(f"No Funk with name '{name}' found.")
        
        return funk.run(input_content, examples, full_resp)

    def show(self):
        return list(self.funks)