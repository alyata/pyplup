import os
import json

"""
Default parsing function, attempts to match the input to formats given
in message_formats.txt. Constructs a dictionary in the following way:
Matched Pattern: |type|PARAM_1|PARAM_2|...|PARAM_N
output: {
    "TYPE" : "type",
    "PARAM_1" : tokens[1],
    ...
    "PARAM_N" : tokens[N]
}
"""

# the directory of this python file
__directory__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# buffer size to hold additional parameters AKA message tags
TAG_SIZE = 2

def read_formats(filename: str) ->[[str]]:
    file_location = os.path.join(__directory__, filename)
    lines = open(file_location, "r").read().split("\n")
    return [line.split('|')[1:] for line in lines if (line and line[0] != '#')]

formats = read_formats("message_formats.txt")

def parse_def(tokens: [str]) -> dict:
    for format_tokens in formats:
        if pattern_match(format_tokens, tokens):
            return build_dict(format_tokens, tokens)
    return unrecognized(tokens)

def pattern_match(format_tokens: [str], tokens: [str]) -> bool:
    #split into a list of type aliases
    types = format_tokens[0].split('/')
    correct_type = tokens[0] in types
    correct_length = len(format_tokens) + TAG_SIZE >= len(tokens)
    return correct_type and correct_length

def build_dict(format_tokens: [str], tokens: [str]) -> dict:
    # Use the first type alias as the primary type name
    types = format_tokens[0].split('/')
    output = {"TYPE" : types[0]}
    # Remove the type label
    format_tokens = format_tokens[1:]
    tokens = tokens[1:]
    # Add tag labels
    format_tokens += [f"TAG {n + 1}" for n in range(TAG_SIZE)]
    # Assign the param values
    for format_token, token in zip(format_tokens, tokens):
        # Check for datatype annotation of param
        subtokens = format_token.split(':')
        if len(subtokens) > 1:
            token = convert_datatype(token, subtokens[1])
        output[subtokens[0]] = token
    return output

def convert_datatype(data: str, type: str):
    return {
        "INT" : lambda d: int(d),
        "JSON" : lambda d: json.loads(d),
    }.get(type, id)(data)

def unrecognized(tokens: [str]) -> dict:
    return {
        "TYPE" : "unrecognized",
        "TOKENS" : tokens,
    }
