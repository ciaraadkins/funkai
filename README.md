# Funkai Library

Funkai is a Python library that encapsulates linguistic operations and uses OpenAI to perform them based on user inputs.

## Features

- Diverse Operations: Easily define linguistic tasks that can process various data types.
- Interaction with OpenAI: Seamlessly connect and utilize the OpenAI API to run operations.
- Dynamic Management: Add, remove, and run operations on-the-fly with the FunkManager.

## Funkai Setup

Install via pip:

```python
pip install funkai
```

Or clone the repository:

```python
git clone https://github.com/ciaraadkins/funkai.git
pip install ./funkai/
```

Once installed, import the necessary modules:

```python
from funkai import FunkManager
```

## OpenAI Setup

For the OpenAI functionality to work, you need to set up your OpenAI API key with init of FunkManager

```python
funk = FunkManager(
        model="gpt-4-turbo-preview",
        api_key='OPEN_API_KEY'
    )
```

Additionally, if you want to monitor your llm usage, we recommend using llmonitor (you will need to also set up an account and get an app id on [llmonitor.com](https://llmonitor.com/)):

```python
pip install openai llmonitor
os.environ["LLMONITOR_APP_ID"] = "YOUR_LLMONITOR_APP_ID"
```

# Methods

###### `add(name, operation, api_key=None, model=None, retry_count=0, input_dtype=str, output_dtype=str)`

Add a new Funk instance to the manager.

#### Parameters:

- `name`: Unique identifier for the Funk instance.
- `operation`: Description of the operation or task performed by the Funk instance.
- `api_key`: API key for accessing the OpenAI GPT API. If not provided, the API key from FunkManager will be used.
- `model`: Model to be used for the Funk instance. If not provided, the default model from FunkManager will be used.
- `retry_count`: Number of retries allowed if there's an error during execution (default is 0).
- `input_dtype`: Data type expected for input to the Funk instance (default is `str`).
- `output_dtype`: Data type expected for output from the Funk instance (default is `str`).

#### Raises:

- `ValueError`: If a Funk with the same name already exists or if the parameters are invalid.

###### `update(name, **kwargs)`

Update parameters of an existing Funk instance.

#### Parameters:

- `name`: Name of the Funk instance to update.

- `**kwargs`: Parameters to update. Supported parameters are `retry_count`, `input_dtype`, `output_dtype`.

#### Raises:

- `ValueError`: If no Funk with the specified name is found or if an invalid parameter is provided.

###### `run(name, input_content, examples=None, full_resp=False)`

Execute a Funk operation by name.

#### Parameters:

- `name`: Name of the Funk instance to run.
- `input_content`: Input data for the Funk operation.
- `examples`: Dictionary of examples to provide context or guidance to the Funk operation (default is `None`).
- `full_resp`: Boolean indicating whether to return the full response including metadata (default is `False`).

#### Returns:

- Output of the Funk operation.

#### Raises:

- `ValueError`: If no Funk with the specified name is found.

## Example Usage

```python
# Initialize FunkManager
manager = FunkManager(model="gpt-4-turbo-preview", api_key="YOUR_OPENAI_API_KEY")

# Add a new Funk instance
manager.add(name="example_funk", operation="Perform a sample task")

# Update parameters of the Funk instance
manager.update("example_funk", retry_count=3, output_dtype=int)

# Run the Funk operation
output = manager.run(name="example_funk", input_content="Input data")

print(output)

## Using Functions (Funks)
## Execute your defined function:

my_funks.run("rhyme5", "cat")
# should return something like: ['bat', 'hat', 'mat', 'rat', 'sat']

items = ["apple", "bike", "carrot", "date", "elephant", "fig", "grape", "helicopter", "ice cream", "jackfruit", "kite", "lemon", "mango", "notebook","strawberry", "television", "umbrella", "van", "watermelon", "xylophone", "yellow", "zebra"]

my_funks.run("find fruit", items)
# should return something like: ['apple','date','fig','grape','jackfruit','lemon','mango','strawberry','watermelon']
```

## Prerequisites

This library is built on top of the OpenAI API. Ensure you have the OpenAI Python client installed and configured.

## Contributing

If you find any bugs or want to propose enhancements, feel free to create issues and pull requests on [GitHub](https://github.com/ciaraadkins/funkai).

## License

This library is under the MIT license. See [LICENSE](./LICENSE) for more details.
