"""
A collection of parsing functions to parse Server-to-Client messages.
As a battle bot, most messages can be ignored. Of particular interest
are messages pertaining to starting battles and logins.
"""

import json

def updateuser(tokens: [str]) -> dict:
    #|updateuser|USER|NAMED|AVATAR|SETTINGS
    return {
        "TYPE"     : tokens[0],
        "USER"     : tokens[1],
        "NAMED"    : int(tokens[2]),
        "AVATAR"   : int(tokens[3]),
        "SETTINGS" : json.loads(tokens[4])
    }


def challstr(tokens: [str]) -> dict:
    #|challstr|CHALLSTR
    #CHALLSTR contains '|' characters
    #so it might have been tokenized wrongly
    challstr = ""
    for token in tokens[1:]:
        challstr += token + "|"
    return {
        "TYPE" : tokens[0],
        "CHALLSTR" : challstr
    }

def formats(tokens: [str]) -> dict:
    #|formats|FORMATSLIST
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
        "TYPE" : tokens[0],
        "FORMATSLIST" : format_sections
    }
