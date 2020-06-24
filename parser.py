"""
A collection of parsing functions to parse Server-to-Client messages.
As a battle bot, most messages can be ignored. Of particular interest
are messages pertaining to starting battles and logins.
"""

import json, re
from itertools import groupby

def updateuser(list_of_strings):
    # |updateuser|USER|NAMED|AVATAR|SETTINGS
    # USER : string, NAMED : int, AVATAR : int, SETTINGS : json
    return {
        "TYPE"     : list_of_strings[0],
        "USER"     : list_of_strings[1],
        "NAMED"    : int(list_of_strings[2]),
        "AVATAR"   : int(list_of_strings[3]),
        "SETTINGS" : json.loads(list_of_strings[4])
    }


def challstr(list_of_strings):
    #|challstr|CHALLSTR
    #nb: CHALLSTR contains '|' characters
    return {
        "TYPE" : list_of_strings[0],
        "CHALLSTR" : "".join(intersperse(list_of_strings[1:]))
    }

def formats(list_of_strings):
    print([list(g) for k, g in groupby(list_of_strings[1:], lambda item: re.fullmatch(',\d', item))])

    return {
        "TYPE" : list_of_strings[0],
        "FORMATSLIST" : list_of_strings[1:]
    }

def intersperse(iterable, delimiter = '|'):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x
