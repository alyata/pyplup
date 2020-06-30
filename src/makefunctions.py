from sys import argv

"""
Small script to generate skeleton for parser.py based on a list of showdown
message formats
"""

def makeparser(format):
    ws = format.split('|')
    ws = ws[1:]
    s = f"#{format}\n"
    s += f"def {ws[0]}(tokens: [str]) -> dict:\n"
    s+= "    return {\n"
    s += f"        \"TYPE\" : \"{ws[0]}\",\n"
    for i, w in enumerate(ws[1:]):
        s += f"        \"{w}\" : tokens[{i+1}],\n"
    s += "    }\n\n"
    return (ws[0], s)

if __name__ == "__main__":
    inp = open("message_formats.txt", "r").read()
    out = open("parser_gen.py", "w")
    out.write('''import json

"""
A collection of parsing functions to parse Server-to-Client messages.
As a battle bot, user messages can be ignored. Of particular interest
are messages pertaining to starting battles and logins.
"""

def parse(roomid: str, message: str) -> dict:
    tokens = message.split('|')
    #remove empty first token
    tokens = tokens[1:]
    type = tokens[0]
    parse_func = {
''')
    lines = inp.split("\n")
    funcs = []
    for line in lines:
        if line and line[0] != '#':
            type, func = makeparser(line)
            out.write(f'        \"{type}\" : {type},\n')
            funcs.append(func)
    out.write('''
    }.get(type, unrecognized)
    parsed = parse_func(tokens)
    parsed["ROOMID"] = roomid
    return parsed

def unrecognized(tokens: [str]) -> dict:
    return {
        "TYPE" : "unrecognized",
    }
''')
    for func in funcs:
        out.write(func)
