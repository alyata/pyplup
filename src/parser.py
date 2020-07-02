import json
from .parser_def import parse_def

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
        "challstr" : challstr,
        "formats" : formats,
        "rule" : rule,
        "poke" : poke,
        "request" : request,
    }.get(type, parse_def)
    parsed = parse_func(tokens)
    parsed["ROOMID"] = roomid
    return parsed

"""
Global messages
"""

#|challstr|CHALLSTR
def challstr(tokens: [str]) -> dict:
    #CHALLSTR contains '|' characters
    #so it might have been tokenized wrongly
    challstr = ""
    for token in tokens[1:-1]:
        challstr += token + "|"
    challstr += tokens[-1]
    return {
        "TYPE" : "challstr",
        "CHALLSTR" : challstr
    }

#|formats|FORMATSLIST
def formats(tokens: [str]) -> dict:
    #group formats by section headers
    format_sections = {}
    new_section = False
    for token in tokens[1:]:
        if new_section:
            current_section = token
            format_sections[current_section] = []
            new_section = False
        elif token[0] == ',':
            new_section = True
        else:
            format_sections[current_section].append(token)
    return {
        "TYPE" : "formats",
        "FORMATSLIST" : format_sections
    }

"""
Pre-battle messages
"""

#|rule|RULE: DESCRIPTION
def rule(tokens: [str]) -> dict:
    rule, description = tokens[1].split(':', 1)
    return {
        "TYPE" : "rule",
        "RULE" : rule,
        "DESCRIPTION" : description
    }

#|poke|PLAYER|DETAILS|ITEM
def poke(tokens: [str]) -> dict:
    output = parse_def(tokens)
    output["DETAILS"] = parse_details(output["DETAILS"])
    return output

#SPECIES{, shiny}{, GENDER}{, L##}
def parse_details(details: str) -> dict:
    details = details.split(", ")
    result = {
        "SPECIES" : details[0],
        "SHINY" : False,
        "GENDER" : None,
        "LEVEL" : 100 #default level
    }
    for detail in details[1:]:
        if detail == "shiny":
            result["SHINY"] = True
        elif detail == "M" or detail == "F":
            result["GENDER"] = detail
        else:
            level = detail[1:]
            result["LEVEL"] = int(level)
    return result

"""
Battle messages
"""

#|request|REQUESt
def request(tokens: [str]) -> dict:
    try:
        request = json.loads(tokens[1])
    except json.decoder.JSONDecodeError:
        request = None
    return {
        "TYPE" : "request",
        "REQUEST" : request
    }
