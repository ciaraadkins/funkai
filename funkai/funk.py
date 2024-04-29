import os
import ast
import openai
import anthropic

class Funk:
    def __init__(self, provider, name, operation, api_key, model, options, retry_count=0, input_dtype=str, output_dtype=str):
        self.name = name
        self.operation = operation
        self.input_dtype = input_dtype
        self.output_dtype = output_dtype
        self.retry_count = retry_count
        self.model = model
        self.error = False
        self.provider = provider
        self.options = options
        self.set_api_key(api_key)
        self.restricted_models(model)

    def set_api_key(self, key):
        if not key:
            raise ValueError("OpenAI API Key not set. Set the key using Funk.set_api_key('YOUR_API_KEY').")
        
        if self.provider == 'openai':
            openai.api_key = key
        else:
            self.api_key = key

        if 'LLMONITOR_APP_ID' in os.environ:
            try:
                from llmonitor import monitor
                monitor(openai)
            except ImportError:
                self.error = True
                print("LLMONITOR_APP_ID is set but llmonitor is not installed. Install llmonitor and rerun.")

    def restricted_models(self, value):
        if self.provider == 'openai':
            restricted_values = ['gpt-3.5-turbo-16k', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo-16k-0613',
                                'gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'gpt-4-0613', 'gpt-3.5-turbo-0301', 
                                'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-instruct-0914', 'gpt-4', 
                                'gpt-3.5-turbo-instruct', 'gpt-4-1106-preview', 'gpt-4-vision-preview',
                                'gpt-4-0125-preview', 'gpt-4-turbo-preview']
        else: 
            restricted_values = ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307']

        if value not in restricted_values:
            print("Model value is not allowed. Please choose from:", restricted_values)
  
    def _prepare_messages(self, sys_cont, examples, input_content):
        user_messages = [
            {"role": "user", "content": f"Operation: {self.operation}\nInput: {str(ex)}\nOutput data type: {self.output_dtype}"}
            for ex in examples
        ]
        user_messages.append({"role": "user", "content": f"Operation: {self.operation}\nInput: {input_content}\nOutput data type: {self.output_dtype}"})
        assistant_messages = [
            {"role": "assistant", "content": ex}
            for ex in examples.values()
        ]
        return [{"role": "system", "content": sys_cont}] + user_messages + assistant_messages

    def _funkai_main(self, sys_cont, examples, input_content):
        messages = self._prepare_messages(sys_cont, examples, input_content)
        max_tokens = 1000 if len(messages) > 1 else 500

        try:
            options = {
                'temperature': self.options.get('temperature', 0.7),
                'max_tokens': self.options.get('max_tokens', max_tokens),
            }

            if self.provider == 'openai':
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    **options
                )
            else:
                client = anthropic.Anthropic(api_key=self.api_key)
                response = client.messages.create(
                    model=self.model,
                    messages=messages,
                    **options
                )

            return response

        except (openai.OpenAIError, Exception) as e:
            if self.retry_count > 0:
                self.retry_count -= 1
                return self._funkai_main(sys_cont, examples, input_content)
            else:
                raise e

    def run(self, input_content, examples=None, full_resp=False):
        if not isinstance(input_content, self.input_dtype):
            raise TypeError(f"Expected input of type {self.input_dtype}, but got {type(input_content)}")

        system_content = """Act as a python program. Process the input based on the operation provided and produce an output. 
        Ensure the output matches the specified Python data type because the result will be interpreted as a Python literal. 
        The output must only be the response with no explanation."""

        examples = examples or {}

        raw_output = self._funkai_main(system_content, examples, str(input_content))
        raw_output_str = Funk._clean_gpt_response(raw_output)

        try:
            converted_output = Funk._convert_output(raw_output_str, self.output_dtype)
            if full_resp:
                return converted_output, raw_output
            else:
                return converted_output
        except ValueError as ve:
            self.error = True
            raise TypeError(f"Failed to convert output to {self.output_dtype}. Raw output: {raw_output_str}. Error: {ve}")


    @staticmethod
    def _clean_gpt_response(response):
        if 'content' in response:
            return response.content
        else:
            return response.choices[0].message.content

    @staticmethod
    def _convert_output(output_str, target_dtype):
        def _convert(eval_func, err_message):
            try:
                return eval_func(output_str)
            except (ValueError, SyntaxError):
                raise ValueError(f"Cannot convert '{output_str}' to {target_dtype}: {err_message}")

        if target_dtype == bool:
            return output_str.lower() in ["true", "yes", "1"]
        elif target_dtype in [list, tuple, set, frozenset, dict]:
            return _convert(ast.literal_eval, "invalid syntax")
        elif target_dtype in [bytes, bytearray, memoryview]:
            return _convert(lambda x: target_dtype(ast.literal_eval(x)), "invalid syntax")
        elif target_dtype == range:
            return _convert(lambda x: range(*ast.literal_eval(x)) if isinstance(ast.literal_eval(x), (list, tuple)) and len(ast.literal_eval(x)) in [1, 2, 3] else ValueError, "invalid range syntax")
        elif target_dtype == str:
            return output_str
        else:
            return _convert(target_dtype, "conversion error")
