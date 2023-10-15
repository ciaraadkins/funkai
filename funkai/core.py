# core.py
# Imports and any global variables/constants
import openai
import ast
import datetime
import os

# Funk Class Definition
class Funk:
    # Methods and functionality for individual Funks
    def __init__(self, name, operation, input_dtype=str, output_dtype=str):
        self.name = name
        self.operation = operation
        self.input_dtype = input_dtype
        self.output_dtype = output_dtype
        self.check_api_key()
        
    @staticmethod
    def set_api_key(key):
        os.environ['OPENAI_API_KEY'] = key
        openai.api_key = key

    @staticmethod
    def check_api_key():
        if not openai.api_key and 'OPENAI_API_KEY' not in os.environ:
            raise ValueError(
                "OpenAI API Key not set. You can set the key in one of the following ways: \n"
                "1. Directly using the OpenAI library: openai.api_key = 'YOUR_API_KEY' \n"
                "2. Setting it as an environment variable: os.environ['OPENAI_API_KEY'] = 'YOUR_API_KEY' \n"
                "3. If you have trouble with the above methods, use Funkai.set_api_key('YOUR_API_KEY'). \n"
                "If you've already done this and still encounter this error, please ensure your API key is correct."
            )
        elif 'LLMONITOR_APP_ID' in os.environ:
            try:
                from llmonitor import monitor
                monitor(openai)
            except:
                print("Looks like you have your 'LLMONITOR_APP_ID' variable set but didn't install llmonitor. Install llmonitor and rerun.")

    def _get_relevant_examples(self, ex):
        """
        Fetches the relevant examples from the examples dictionary based on input_dtype and output_dtype.

        Args:
        - examples (dict): The dictionary containing all examples.

        Returns:
        - list: A list of relevant examples based on input and output data types.
        """
        # Generate the keys based on the input and output data types
        input_key = "in_" + self.input_dtype.__name__
        output_key = "out_" + self.output_dtype.__name__

        try:
            # Fetch the examples using the generated keys
            relevant_examples = ex[input_key][output_key]
            # print("relevant_examples: "+str(relevant_examples))
            return relevant_examples
        except KeyError:
            # No examples found for the given data types
            return []

    def _funkai_main(self, sys_cont, ex,input):
        """
        Generates a function response based on the provided prompt.

        Args:
        - prompt (str): The prompt for the function.

        Returns:
        - str: The response from the OpenAI model.
        """

        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": sys_cont},
                {"role": "user", "content": input}
                ],
            temperature=0,
            max_tokens=16000)

        return gpt_response

    def run(self, input, print_cost=False):
        """
        Uses a predefined operation to get a response based on input.
        """

        # Check valid input data types
        if not isinstance(input, (dict, list, str)):
            raise TypeError(f"Invalid input type {type(input)}. Expected one of [dict, list, str].")

        # Check input data types
        if not isinstance(input, self.input_dtype):
            raise TypeError(f"Expected input of type {self.input_dtype}, but got {type(input)}")


        system_content = """Act as a python program. Based on the operation provided, process the input and produce an output. Prioritize precision and correctness in your output.
        Note: Ensure the output matches the specified Python data type because the result will be interpreted as a Python literal. The output must only be the response with no explanation. If unsure, return 'None'.
        """
        
        # Check if it's a string
        if isinstance(input, str):
            str_input = input
        else:
            str_input = str(input)

        formatted_input = f"Operation: {self.operation}\nInput: {input}\nOutput data type: {self.output_dtype}"
        the_examples = self._get_relevant_examples(all_prompts)
        raw_output = self._funkai_main(system_content,the_examples,formatted_input)
        raw_output_str = Funk._clean_gpt_response(raw_output)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Convert the output to the desired data type
        try:
            return Funk._convert_output(raw_output_str, self.output_dtype)
        except ValueError:
            raise TypeError(f"Failed to convert output to {self.output_dtype}. Raw output: {raw_output_str}")

    @staticmethod
    def _clean_gpt_response(response):
        model = response['model']
        if model == "gpt-3.5-turbo-instruct":
            text = response['choices'][0]['text']
            return text
        elif model.startswith("gpt-3.5-turbo"):
            text = response['choices'][0]['message']['content']
            return text
        elif model.startswith("text-davinci"):
            text = response['choices'][0]['text']
            return text
        else:
            print("Not 'gpt-3.5' or 'davinci' model")
            return

    @staticmethod
    def _convert_output(output_str, target_dtype):
        """
        Convert the raw output string to the desired data type.
        Handle special cases for common data types.
        """
        if target_dtype == bool:
            if output_str.lower() in ["true", "yes", "1"]:
                return True
            elif output_str.lower() in ["false", "no", "0"]:
                return False
            else:
                raise ValueError(f"Cannot convert '{output_str}' to bool")
        
        elif target_dtype in [list, tuple, set, frozenset, dict]:
            try:
                # Convert string representation to actual data structure
                return target_dtype(ast.literal_eval(output_str))
            except (ValueError, SyntaxError):
                raise ValueError(f"Cannot convert '{output_str}' to {target_dtype}")

        elif target_dtype == bytes:
            try:
                # Convert string representation of bytes (b'...') to actual bytes
                return ast.literal_eval(output_str)
            except (ValueError, SyntaxError):
                raise ValueError(f"Cannot convert '{output_str}' to bytes")

        elif target_dtype == bytearray:
            try:
                # Convert string representation of bytes (b'...') to actual bytearray
                return bytearray(ast.literal_eval(output_str))
            except (ValueError, SyntaxError):
                raise ValueError(f"Cannot convert '{output_str}' to bytearray")
        
        elif target_dtype == memoryview:
            try:
                # Convert string representation of bytes (b'...') to actual memoryview
                return memoryview(ast.literal_eval(output_str))
            except (ValueError, SyntaxError):
                raise ValueError(f"Cannot convert '{output_str}' to memoryview")

        elif target_dtype == range:
            try:
                # Convert string representation of list/tuple to range
                items = ast.literal_eval(output_str)
                if not isinstance(items, (list, tuple)) or len(items) not in [1, 2, 3]:
                    raise ValueError
                return range(*items)
            except (ValueError, SyntaxError):
                raise ValueError(f"Cannot convert '{output_str}' to range")
        
        # For basic types like int, float, str, complex
        try:
            return target_dtype(output_str)
        except ValueError:
            raise ValueError(f"Cannot convert '{output_str}' to {target_dtype}")

# FunkManager Class Definition
class FunkManager:
    # Methods for managing and operating on multiple Funks
    def __init__(self):
        self.funks = {}  # Store the Funk instances by name

    def add(self, name, operation, input_dtype=str, output_dtype=str):
        if name in self.funks:
            raise ValueError(f"A Funk with name '{name}' already exists.")
        new_funk = Funk(name, operation, input_dtype, output_dtype)
        self.funks[name] = new_funk

    def _get(self, name):
        return self.funks.get(name, None)

    def remove(self, name):
        if name not in self.funks:
            raise ValueError(f"No Funk with name '{name}' found.")
        del self.funks[name]

    def run(self, name, input, print_cost=False):
        funk = self._get(name)
        if not funk:
            raise ValueError(f"No Funk with name '{name}' found.")
        return funk.run(input, print_cost)

    def show(self):
        return list(self.funks.keys())