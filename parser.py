"""
A collection of parsing functions to parse Server-to-Client messages.
As a battle bot, most messages can be ignored. Of particular interest
are messages pertaining to starting battles and logins.
"""

import json

def updateuser(tokens):
    #|updateuser|USER|NAMED|AVATAR|SETTINGS
    return {
        "TYPE"     : tokens[0],
        "USER"     : tokens[1],
        "NAMED"    : int(tokens[2]),
        "AVATAR"   : int(tokens[3]),
        "SETTINGS" : json.loads(tokens[4])
    }


def challstr(tokens):
    #|challstr|CHALLSTR
    #note: CHALLSTR contains '|' characters
    challstr = ""
    for token in tokens[1:]:
        challstr += token + "|"
    return {
        "TYPE" : tokens[0],
        "CHALLSTR" : challstr
    }

def formats(tokens):
    #|formats|
    return {
        "TYPE" : tokens[0],
        "FORMATSLIST" : tokens[1:]
    }
