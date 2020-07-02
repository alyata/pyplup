import os
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

__directory__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

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
    return format_tokens[0] == tokens[0] and len(format_tokens) == len(tokens)

def build_dict(format_tokens: [str], tokens: [str]) -> dict:
    output = {"TYPE" : format_tokens[0]}
    # Remove the type label
    format_tokens = format_tokens[1:]
    tokens = tokens[1:]
    # Assign the param values
    for n, format_token in enumerate(format_tokens):
        output[format_token] = tokens[n]
    return output

def unrecognized(tokens: [str]) -> dict:
    return {
        "TYPE" : "unrecognized",
        "TOKENS" : tokens,
    }
