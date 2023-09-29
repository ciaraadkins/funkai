################################################################
# ************************ INPUT: DICT* ************************
################################################################
in_dict_short = {
    "name": "Alice",
    "profession": "astronomer",
    "favorite_fruit": "apple",
    "mode_of_transport": "bicycle",
    "hobby": "reading"
}

in_dict_long = {
    "rose": "flower",
    "sparrow": "bird",
    "watch": "timepiece",
    "laptop": "computer",
    "carrot": "vegetable",
    "telescope": "astronomy",
    "comet": "space",
    "apple": "fruit",
    "lorry": "vehicle",
    "eagle": "raptor",
    "ferry": "boat"
}

new_dict_short = {
    "name": "John",
    "profession": "teacher",
    "favorite_fruit": "mandarin orange",
    "mode_of_transport": "car",
    "hobby": "knitting"
}

in_dict = {
        "out_bool": {
            "example1": {
                "prompt": f"Operation: determine if all the keys in the dictionary are related to nature\nInput: {str(in_dict_short)}\nOutput data type: bool",
                "response": False
            },
            "example2": {
                "prompt": f"Operation: check if the dictionary represents a coherent theme or category\nInput: {str(in_dict_long)}\nOutput data type: bool",
                "response": True
            }
        },
        "out_dict": {
            "example1": {
                "prompt": f"Operation: Extract only the key-value pairs where the value represents a profession or hobby\nInput: {str(in_dict_short)}\nOutput data type: dict",
                "response": {
                    "profession": "astronomer",
                    "hobby": "reading"
                }
            },
            "example2": {
                "prompt": f"Operation: create a dictionary with the same keys but new values\nInput: {str(in_dict_short)}\nOutput data type: dict",
                "response": new_dict_short
            }
        },
        "out_list": {
            "example1": {
                "prompt": f"Operation: return a list of all keys or values in the dictionary that are related to space or astronomy\nInput: {str(in_dict_long)}\nOutput data type: list",
                "response": ["astronomy", "space", "telescope", "comet"]
            },
            "example2": {
                "prompt": f"Operation: Return all keys where their corresponding value is a type of transport\nInput: {str(in_dict_long)}\nOutput data type: list",
                "response": ["ferry", "lorry"]
            }
        },
        "out_str": {
            "example1": {
                "prompt": f"Operation: describe the most frequently appearing theme in the dictionary values\nInput: {str(in_dict_long)}\nOutput data type: str",
                "response":"Nature"
            },
            "example2": {
                "prompt": f"Operation: create a personalized pun greeting based on the user's interests\nInput: {str(in_dict_short)}\nOutput data type: str",
                "response": "Hey Alice, hope you're having a stellar day!"
            }
        }
}


################################################################
# ************************ INPUT: LIST* ************************
################################################################
in_list_long = ["apple", "bicycle", "cat", "date", "eagle", "ferry", "grapefruit", "helicopter", "iguana", "jackfruit", "kangaroo", "lorry", "mango", "notebook", "ostrich"]
in_list_short = ["rose", "sparrow", "watch", "laptop", "carrot"]
astronomy_list = ["telescope", "planet", "star", "galaxy", "comet", "nebula", "black hole", "constellation", "asteroid", "supernova", "solar system", "space probe", "observatory", "eclipse", "satellite"]
fruit_list = ["apple", "banana", "car"]
related_words = {
    "apple": "fruit",
    "bicycle": "pedal",
    "cat": "feline",
    "date": "calendar",
    "eagle": "bird",
    "ferry": "boat",
    "grapefruit": "citrus",
    "helicopter": "rotor",
    "iguana": "reptile",
    "jackfruit": "tropical",
    "kangaroo": "marsupial",
    "lorry": "truck",
    "mango": "sweet",
    "notebook": "paper",
    "ostrich": "flightless"
}

in_list = {
        "out_bool": {
            "example1": {
                "prompt": f"Operation: determine if the items in the list form a coherent story or theme\nInput: {str(in_list_long)}\nOutput data type: bool",
                "response": False
            },
            "example2": {
                "prompt": f"Operation: are there fruits in the list\nInput: {str(fruit_list)}\nOutput data type: bool",
                "response": True
            }
        },
        "out_dict": {
            "example1": {
                "prompt": f"Operation: group items in the list by their sentiment (positive, neutral, negative)\nInput: {str(in_list_short)}\nOutput data type: dict",
                "response": {
                    "positive": ["rose", "sparrow"],
                    "neutral": ["watch", "laptop", "carrot"]
                }
            },
            "example2": {
                "prompt": f"Operation: For each item, provide a related word\nInput: {str(in_list_long)}\nOutput data type: dict",
                "response": related_words
            }
        },
        "out_list": {
            "example1": {
                "prompt": f"Operation: Return a list of items in the reverse order of their importance in a survival situation\nInput: {str(in_list_long)}\nOutput data type: list",
                "response": ["notebook", "television", "apple", "mango", "water"]  # Just a hypothetical order
            },
            "example2": {
                "prompt": f"Operation: given the input list of miscellaneous items, find the electronics\nInput: {str(in_list_short)}\nOutput data type: list",
                "response": ["watch","laptop"]
            }
        },
        "out_str": {
            "example1": {
                "prompt": f"Operation: Summarize the theme of the list in one word\nInput: {str(astronomy_list)}\nOutput data type: str",
                "response": {
                    "str": "Astronomy"
                }
            },
            "example2": {
                "prompt": f"Operation: form a coherent sentence using all the items in the list\nInput: {str(in_list_long)}\nOutput data type: str",
                "response": {
                    "str": "The eagle perched on the bicycle by the mango tree, eyeing the iguana that was munching on a notebook near the lorry."
                }
            }
        }
}

################################################################
# ************************ INPUT: STR ************************
################################################################
alice_greeting = "Hey Alice, hope you're having a stellar day in the world of astronomy! Remember, an apple a day keeps the black holes at bay, especially when you cycle through your reading galaxy!"
alice_adventure = "Alice looked up at the night sky, her telescope in hand, ready for another night of stargazing. As she adjusted the lens, she noticed something unusual."
adventure_response = """
1. Adventure 1: Alice focused her telescope on the unusual sight and was amazed to discover a new celestial body moving across the sky. This wasn't any ordinary star or planet - it shimmered with a rainbow of colors. With notes and sketches, she spent the entire night documenting this discovery. The next day, her findings drew the attention of astronomers worldwide, leading her to collaborate with top experts and cementing her place in the annals of astronomy.
2. Adventure 2: The shimmering object in the sky suddenly started growing bigger and brighter. To Alice's astonishment, it was an alien spacecraft descending! The craft landed nearby, and out came beings from another world. They were peaceful explorers, wanting to learn about Earth and its inhabitants. Thanks to Alice's love for reading and her vast knowledge, she was able to communicate with them and act as Earth's ambassador, turning an ordinary night of stargazing into a historic interstellar diplomatic event.
"""

amazon_sentence = "The Amazon rainforest is the world's largest tropical rainforest. It's renowned for its incredible biodiversity and vital ecological role."
story_string = "Once upon a time in a city filled with bicycles and mango trees, a cat named Ostrich decided to write its story in a notebook."
song_lyrics = "Fly eagle fly, soar above the ferry, past the notebook tower, where the iguana plays with a jackfruit."

in_str = {
    "out_bool": {
        "example1": {
            "prompt": f"Operation: Check if the given string is a greeting\nInput: {alice_greeting}\nOutput data type: bool",
            "response": True
        },
        "example2": {
            "prompt": f"Operation: determine if the given string mentions any fruits\nInput: {song_lyrics}\nOutput data type: bool",
            "response": False
        }
    },
    "out_dict": {
        "example1": {
          "prompt": f"Operation: Extract all animals and modes of transportation\nInput: {story_string}\nOutput data type: dict",
          "response": {
              "animals": ["cat","ostrich"],
              "transportation":["bicycle"],
          }
        },
        "example2": {
            "prompt": f"Operation: identify the actions done by each subject in the sentence\nInput: 'John runs fast. Maria sings beautifully. The dog barks loudly.'\nOutput data type: dict",
            "response": {
                "John": "runs",
                "Maria": "sings",
                "dog": "barks"
            }
        }
    },
    "out_list": {
        "example1": {
            "prompt": f"Operation: extract a list of all items that could be considered stationary\nInput: {story_string}\nOutput data type: list",
            "response": ["notebook"]
        },
        "example2": {
            "prompt": f"Operation: Identify the primary themes/topics of the string\nInput: {amazon_sentence}\nOutput data type: list",
            "response": ["Amazon rainforest", "biodiversity", "ecology"]
        }
    },
    "out_str": {
        "example1": {
            "prompt": f"Operation: Extract the name of the main character\nInput: {story_string}\nOutput data type: str",
            "response": "Ostrich"
        },
        "example2": {
            "prompt": f"Operation: given the start of an adventure, play out 2 different adventures that could result\nInput: {alice_adventure}\nOutput data type: str",
            "response": adventure_response
        }
    }
}

################################################################
# ************************ CONSOLIDATE ************************
################################################################
all_prompts = {
    "in_dict": in_dict,
    "in_list": in_list,
    "in_str": in_str
}