"""
Small script to generate skeleton for parser.py based on a list of showdown
message formats
"""

def makeparser(format):
    ws = format.split('|')
    ws = ws[1:]
    #remove dashes, as python symbols can't have dashes
    fname = f'generated_{ws[0].replace("-", "_")}'
    #construct the function
    s = f"#{format}\n"
    s += f"def {fname}(tokens: [str]) -> dict:\n"
    s+= "    return {\n"
    s += f"        \"TYPE\" : \"{ws[0]}\",\n"
    for i, w in enumerate(ws[1:]):
        s += f"        \"{w}\" : tokens[{i+1}],\n"
    s += "    }\n\n"
    return (ws[0], fname, s)

if __name__ == "__main__":
    inp = open("message_formats.txt", "r").read()
    out = open("parser_gen.py", "w")
    out.write('''def parse_gen(tokens: [str]) -> dict:
    parse_func = {
''')
    lines = inp.split("\n")
    funcs = []
    for line in lines:
        if line and line[0] != '#':
            type, fname, func = makeparser(line)
            out.write(f'        \"{type}\" : {fname},\n')
            funcs.append(func)
    out.write('''
    }.get(tokens[0], unrecognized)
    parsed = parse_func(tokens)
    return parsed

def unrecognized(tokens: [str]) -> dict:
    return {
        "TYPE" : "unrecognized",
    }
    
''')
    for func in funcs:
        out.write(func)
