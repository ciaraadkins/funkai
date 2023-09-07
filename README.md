# Funkai

Easily create and use placeholder functions powered by the OpenAI API. Ideal for prototyping and quickly mocking up functionality.

## Installation

```bash
pip install funkai

## Quickstart

1. **Define a Pre-set Function**

    Use the `add_funk` function to create a pre-defined operation. 

    ```python
    from funkai.core import add_funk

    add_funk(
        name="animal_sound",
        operation="respond with the sound the given animal makes",
        input_dtype=str,
        output_dtype=str
    )
    ```

2. **Use the Pre-defined Function**

    After defining a preset, use the `funktion` method to generate a response.

    ```python
    from funkai.core import funktion

    response = funktion("cat", funk="animal_sound")
    print(response)  # E.g., "meow"
    ```

## Features

- **Simple Interface**: With just two primary functions (`add_funk` and `funktion`), the library is easy to use and understand.
- **Data Type Validation**: Ensures inputs and outputs adhere to predefined data types.
- **Powered by OpenAI**: Leverage the power of GPT-3.5-turbo or any other model from OpenAI's offerings.

## Documentation

### `funktion(input, funk)`

Uses a predefined operation to generate a response based on the input.

- `input`: The input data.
- `funk`: The name of the predefined function to be used.

### `add_funk(name, operation, input_dtype, output_dtype)`

Define a new preset function.

- `name`: The name of the function preset.
- `operation`: The description of the function's purpose.
- `input_dtype`: The data type for input arguments.
- `output_dtype`: The expected data type for the output.

## Prerequisites

This library is built on top of the OpenAI API. Ensure you have the OpenAI Python client installed and configured.


## Contributing

If you find any bugs or want to propose enhancements, feel free to create issues and pull requests on [GitHub](https://github.com/ciaraadkins/funkai).

## License

This library is under the MIT license. See [LICENSE](./LICENSE) for more details.


