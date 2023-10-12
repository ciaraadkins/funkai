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
from funkai import Funk,FunkManager
```

## OpenAI Setup
For the OpenAI functionality to work, you need to set up your OpenAI API key:
```python
import openai
import os

# Replace with your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'
```

Additionally, if you want to monitor your llm usage we recommend using llmonitor (you will need to also set up an account and get an app id on https://llmonitor.com/:
```python
pip install openai llmonitor
os.environ["LLMONITOR_APP_ID"] = "YOUR_LLMONITOR_APP_ID"
```

# Quick Start
## Defining Functions (Funks)
Add functions as per your requirements:
```python
my_funks = FunkManager()

my_funks.add(
    name="rhyme5",
    operation="given a word, generate 5 words that rhyme with it.",
    input_dtype=str,
    output_dtype=list
)

fruit_finder = my_funks.add(
    name="find fruit",
    operation="given the input list of miscellaneous items, return a list of only the fruit",
    input_dtype=list,
    output_dtype=list
)
```

## Using Functions (Funks)
Execute your defined function:
```python
my_funks.run("rhyme5", "cat"))
# should return something like: ['bat', 'hat', 'mat', 'rat', 'sat']

items = ["apple", "bike", "carrot", "date", "elephant", "fig", "grape", "helicopter", "ice cream", "jackfruit", "kite", "lemon", "mango", "notebook","strawberry", "television", "umbrella", "van", "watermelon", "xylophone", "yellow", "zebra"]
my_funks.run("find fruit",items)
# should return something like: ['apple','date','fig','grape','jackfruit','lemon','mango','strawberry','watermelon']
```

## Prerequisites

This library is built on top of the OpenAI API. Ensure you have the OpenAI Python client installed and configured.


## Contributing

If you find any bugs or want to propose enhancements, feel free to create issues and pull requests on [GitHub](https://github.com/ciaraadkins/funkai).

## License

This library is under the MIT license. See [LICENSE](./LICENSE) for more details.


