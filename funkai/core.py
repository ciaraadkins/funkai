# core.py
# Imports and any global variables/constants
import openai
import ast
import datetime
import os
from .examples import all_prompts

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

    def get_cost(self):
        return self.cost_information

    # def _funkai_main_exp(self, prompt):
    #     """
    #     Generates a function response based on the provided prompt.

    #     Args:
    #     - prompt (str): The prompt for the function.

    #     Returns:
    #     - str: The response from the OpenAI model.
    #     """
    #     # response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)

    #     gpt_response = openai.Completion.create(
    #         model="gpt-3.5-turbo-instruct",
    #         prompt=prompt,
    #         temperature=0,
    #         max_tokens=4096
    #         )

    #     return gpt_response
    
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
        
        print("input_key: "+input_key)
        print("output_key: "+output_key)

        try:
            # Fetch the examples using the generated keys
            relevant_examples = ex[input_key][output_key]
            print("relevant_examples: "+str(relevant_examples))
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
        # response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)

        print("examples in _funkai_main: "+str(ex))

        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            # model="gpt-4-32k",
            messages=[
                {"role": "system", "content": sys_cont},
                {"role": "user", "content": ex['example1']['prompt']},
                {"role": "assistant", "content": str(ex['example1']['response'])},
                {"role": "user", "content": ex['example2']['prompt']},
                {"role": "assistant", "content": str(ex['example2']['response'])},
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

        formatted_input = f"Operation: {self.operation}\nInput: {input}\nOutput data type: {self.output_dtype}"
        the_examples = self._get_relevant_examples(all_prompts)
        print("the_examples: "+str(the_examples))
        raw_output = self._funkai_main(system_content,the_examples,formatted_input)
        raw_output_str = Funk._clean_gpt_response(raw_output)

        # raw_output = self._funkai_main(prompt)
        # raw_output_str = Funk._clean_gpt_response(raw_output)
        
        # get cost info
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cost_for_this_run, tokens_used = Funk._approx_cost(raw_output)

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
            # Print information about the current run
            print("\n--- Current Run Information ---")
            print(f"Tokens used for this call: {tokens_used}")
            print(f"Approximate cost for this call: ${cost_for_this_run:.2f}")
            
            # Print cumulative totals for the session
            print("\n--- Session Totals ---")
            print(f"Total tokens used this session: {self.cost_information['total_tokens']}")
            print(f"Approximate total cost for this session: ${self.cost_information['approx_total_cost']:.2f}")
            print("-----------------------------\n") # To separate the output

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

    # def print_approx_cost(self):
    #     """Prints the accumulated cost information for the session."""
    #     # ... (Content remains the same, but maybe store cost info at the instance level too)

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

    def get(self, name):
        return self.funks.get(name, None)

    def remove(self, name):
        if name not in self.funks:
            raise ValueError(f"No Funk with name '{name}' found.")
        del self.funks[name]

    def run(self, name, input, print_cost=False):
        funk = self.get(name)
        if not funk:
            raise ValueError(f"No Funk with name '{name}' found.")
        return funk.run(input, print_cost)

    def list_all(self):
        return list(self.funks.keys())

    # def cost(self):
    #     return self.get_cost()

####################################
# ******** USAGE EXAMPLES ********
####################################
# manager = FunkManager()
# manager.add_funk(name="test", operation="do something")
# result = manager.run_funk(name="test", input="Some input here")
# print(result)
# print(manager.list_all_funks())