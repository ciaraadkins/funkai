# core.py

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

# text = getTextResponse(response)

def funktion(input, funk):
    """
    Uses a predefined operation to get a response based on input.
    """
    
    preset = FUNKAI_PRESETS.get(funk)
    if not preset:
        raise ValueError(f"Preset '{funk}' not found.")
    
    operation = preset["operation"]
    input_dtype = preset["input_dtype"]
    output_dtype = preset["output_dtype"]

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
        return output_dtype(raw_output_str)
    except ValueError:
        raise TypeError(f"Failed to convert output to {output_dtype}. Raw output: {raw_output_str}")

def add_funk(name, operation, input_dtype, output_dtype):
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
