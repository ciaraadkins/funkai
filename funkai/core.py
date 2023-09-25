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

        # Cost tracking for this specific Funk instance
        self.cost_information = {
            "runs": [],
            "total_tokens": 0,
            "approx_total_cost": 0.0  # Placeholder
        }
        
    @staticmethod
    def set_api_key(key):
        if use_env_var:
            os.environ['OPENAI_API_KEY'] = key
        else:
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

    @staticmethod
    def _approx_cost(response):
        model = response['model']
        prompt_tokens = response['usage']['prompt_tokens']
        completion_tokens = response['usage']['completion_tokens']
        if model.startswith("gpt-3.5-turbo"):
            cost_in= 0.0015/1000 # dollars per token
            cost_out= 0.002/1000 # dollars per token
            tot_tokens = prompt_tokens + completion_tokens
            tot_cost = (cost_in*prompt_tokens) + (cost_out*completion_tokens)
            return tot_cost,tot_tokens
        elif model.startswith("text-davinci"):
            cost_tot = 0.02/1000 # dollars per token
            tot_tokens = prompt_tokens + completion_tokens
            return cost_tot*tot_tokens,tot_tokens
        # elif model is langchain:
        #   use langchain pricing model
        else:
            print("Not 'gpt-3.5' or 'davinci' model")
            return

        return gpt_response

    def run(self, input, print_cost=False):
        """
        Uses a predefined operation to get a response based on input.
        """

        # Check input data types
        if not isinstance(input, self.input_dtype):
            raise TypeError(f"Expected input of type {self.input_dtype}, but got {type(input)}")

        system_content = f"""
        Task Description: Act as a python function whose purpose is to {self.operation}. The function should take an {self.input_dtype} as an input and return an {self.output_dtype} as an output.
        Note: Your output must only be the expected response from the python function with no explanation. If you cannot determine what to output, return 'None'.
        """

        raw_output = funkai_main(system_content, input)
        raw_output_str = clean_gpt_response(raw_output)

        # get cost info
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cost_for_this_run, tokens_used = approxCost(raw_output)

        self.cost_information["runs"].append({
            "timestamp": timestamp,
            "funk_name": self.name,
            "tokens_used": tokens_used,
            "approx_cost": cost_for_this_run
        })

        # Update the total tokens and approximate cost
        self.cost_information["total_tokens"] += tokens_used
        self.cost_information["approx_total_cost"] += cost_for_this_run

        if print_cost:
            print(f"Tokens used for this call: {tokens_used}")
            print(f"Total tokens used this session: {cost_information['total_tokens']}")
            print(f"Approximate cost for this session: ${cost_information['approx_total_cost']:.2f}")

        # Convert the output to the desired data type
        try:
            return convert_output(raw_output_str, self.output_dtype)
        except ValueError:
            raise TypeError(f"Failed to convert output to {self.output_dtype}. Raw output: {raw_output_str}")

    @staticmethod
    def _clean_gpt_response(response):
        model = response['model']
        if model.startswith("gpt-3.5-turbo"):
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

    def print_approx_cost(self):
        """Prints the accumulated cost information for the session."""
        # ... (Content remains the same, but maybe store cost info at the instance level too)

# FunkManager Class Definition
class FunkManager:
    # Methods for managing and operating on multiple Funks
    def __init__(self):
        self.funks = {}  # Store the Funk instances by name

    def add_funk(self, name, operation, input_dtype=str, output_dtype=str):
        if name in self.funks:
            raise ValueError(f"A Funk with name '{name}' already exists.")
        new_funk = Funk(name, operation, input_dtype, output_dtype)
        self.funks[name] = new_funk

    def get_funk(self, name):
        return self.funks.get(name, None)

    def remove_funk(self, name):
        if name not in self.funks:
            raise ValueError(f"No Funk with name '{name}' found.")
        del self.funks[name]

    def run_funk(self, name, input, print_cost=False):
        funk = self.get_funk(name)
        if not funk:
            raise ValueError(f"No Funk with name '{name}' found.")
        return funk.run(input, print_cost)

    def list_all_funks(self):
        return list(self.funks.keys())

####################################
# ******** USAGE EXAMPLES ********
####################################
# manager = FunkManager()
# manager.add_funk(name="test", operation="do something")
# result = manager.run_funk(name="test", input="Some input here")
# print(result)
# print(manager.list_all_funks())