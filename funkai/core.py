# core.py

import openai
import ast

FUNKAI_PRESETS = {}  # Empty dictionary to hold predefined functions

def funkai_main(sys_cont,input):
    """
    Generates a function response based on the provided prompt.

    Args:
    - prompt (str): The prompt for the function.

    Returns:
    - str: The response from the OpenAI model.
    """
    # response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)

    gpt_response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      temperature=0,
      messages=[
          {"role": "system", "content": sys_cont},
          {"role": "user", "content": f"Given the input is '{input}' what should the output of a function be?"}
        ])

    return gpt_response

def funktion(input, funk):
    """
    Uses a predefined operation to get a response based on input.
    """
    
    preset = FUNKAI_PRESETS.get(funk)
    if not preset:
        raise ValueError(f"Preset '{funk}' not found.")
    
    operation = preset["operation"]
    input_dtype = preset.get("input_dtype", str)
    output_dtype = preset.get("output_dtype", str)

    # Check input data types
    if not isinstance(input, input_dtype):
        raise TypeError(f"Expected input of type {input_dtype}, but got {type(input)}")

    system_content = f"""
      Task Description: Act as a python function whose purpose is to {operation}. The function should take an {input_dtype} as an input and return an {output_dtype} as an output.
      Note: Your output must only be the expected response from the python function with no explanation. If you cannot determine what to output, return 'None'.
      """

    # prompt = f"Given the inputs {args} and {kwargs}, what should the output of a function be?"
    raw_output = funkai_main(system_content,input)

    raw_output_str = clean_gpt_response(raw_output)
    
    # Convert the output to the desired data type
    try:
        return convert_output(raw_output_str, output_dtype)
    except ValueError:
        raise TypeError(f"Failed to convert output to {output_dtype}. Raw output: {raw_output_str}")

def add_funk(name, operation, input_dtype=str, output_dtype=str):
    """
    Adds a predefined function to the FUNKAI_PRESETS.
    """
    if name in FUNKAI_PRESETS:
        raise ValueError(f"Preset '{name}' already exists. Choose a different name or overwrite explicitly.")
    
    FUNKAI_PRESETS[name] = {
        "operation": operation,
        "input_dtype": input_dtype,
        "output_dtype": output_dtype
    }

def update_funk(name, operation=None, input_dtype=None, output_dtype=None):
    """
    Updates a specific preset in FUNKAI_PRESETS.
    Args:
    - name (str): The name of the preset to update.
    - operation (str, optional): The new operation description.
    - input_dtype (type, optional): The new expected input data type.
    - output_dtype (type, optional): The new expected output data type.
    """
    preset = FUNKAI_PRESETS.get(name)
    
    if not preset:
        raise ValueError(f"Preset '{name}' not found.")
    
    if operation:
        preset["operation"] = operation
    if input_dtype:
        preset["input_dtype"] = input_dtype
    if output_dtype:
        preset["output_dtype"] = output_dtype
    
    FUNKAI_PRESETS[name] = preset

def remove_funk(name):
    """
    Removes a predefined function from the FUNKAI_PRESETS.

    Args:
    - name (str): The name of the function preset to remove.

    Raises:
    - ValueError: If the preset with the given name is not found.
    """
    if name not in FUNKAI_PRESETS:
        raise ValueError(f"Preset '{name}' not found. Cannot remove.")
    
    del FUNKAI_PRESETS[name]

def funk_details(name=None):
    """
    Returns a specific preset or all presets in FUNKAI_PRESETS.
    
    Args:
    - name (str, optional): The name of the preset to retrieve.
    
    Returns:
    - dict or str: Either the specified preset, all presets, or an error message.
    """
    
    if name:
        preset = FUNKAI_PRESETS.get(name)
        if not preset:
            return f"Preset '{name}' not found."
        return {name: preset}
    
    # If name is not provided, return all presets
    return FUNKAI_PRESETS

# https://openai.com/pricing
# https://platform.openai.com/docs/models

def clean_gpt_response(response):
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

def convert_output(output_str, target_dtype):
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
