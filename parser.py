"""
A collection of parsing functions to parse Server-to-Client messages.
As a battle bot, user messages can be ignored. Of particular interest
are messages pertaining to starting battles and logins.
"""

import json

"""
Room initialization
"""

#|init|ROOMTYPE
def init(tokens: [str]) -> dict:
    return {
        "TYPE" : tokens[0],
        "ROOMTYPE" : tokens[1]
    }

#|title|TITLE
def title(tokens: [str]) -> dict:
    return {
        "TYPE" : tokens[0],
        "TITLE" : tokens[1]
    }

#|users|USERLIST
def users(tokens: [str]) -> dict:
    return {
        "TYPE" : tokens[0],
        "TITLE" : json.loads(tokens[1])
    }

"""
Room messages
"""
#|join|USER or |j|USER or |J|USER
def join(tokens: [str]) -> dict:
    return {
        "TYPE" : "join",
        "TITLE" : tokens[1]
    }

#|leave|USER or |l|USER or |L|USER
def leave(tokens: [str]) -> dict:
    return {
        "TYPE" : "leave",
        "TITLE" : tokens[1]
    }

#|battle|ROOMID|USER1|USER2 or |b|ROOMID|USER1|USER2
def battle(tokens: [str]) -> dict:
    return {
        "TYPE" : "battle",
        "ROOMID" : tokens[1],
        "USER1" : tokens[2],
        "USER2" : tokens[3]
    }

"""
Global messages
"""

#|usercount|USERCOUNT
def usercount(tokens: [str]) -> dict:
    return {
        "TYPE" : tokens[0],
        "USERCOUNT" : int(tokens[1])
    }

#|nametaken|USERNAME|MESSAGE
def nametaken(tokens: [str]) -> dict:
    return {
        "TYPE" : tokens[0],
        "USERNAME" : tokens[1],
        "MESSAGE" : tokens[2]
    }

#|challstr|CHALLSTR
def challstr(tokens: [str]) -> dict:
    #CHALLSTR contains '|' characters
    #so it might have been tokenized wrongly
    challstr = ""
    for token in tokens[1:]:
        challstr += token + "|"
    return {
        "TYPE" : tokens[0],
        "CHALLSTR" : challstr
    }

#|updateuser|USER|NAMED|AVATAR|SETTINGS
def updateuser(tokens: [str]) -> dict:
    return {
        "TYPE"     : tokens[0],
        "USER"     : tokens[1],
        "NAMED"    : int(tokens[2]),
        "AVATAR"   : int(tokens[3]),
        "SETTINGS" : json.loads(tokens[4])
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
        "TYPE" : tokens[0],
        "FORMATSLIST" : format_sections
    }

#|updatesearch|JSON
def updatesearch(tokens: [str]) -> dict:
    return {
        "TYPE" : tokens[0],
        "JSON" : json.loads(tokens[1])
    }

#|updatechallenges|JSON
def updatechallenges(tokens: [str]) -> dict:
    return {
        "TYPE" : tokens[0],
        "JSON" : json.loads(tokens[1])
    }

#|queryresponse|QUERYTYPE|JSON
def queryresponse(tokens: [str]) -> dict:
    return {
        "TYPE" : tokens[0],
        "QUERYTYPE" : tokens[1],
        "JSON" : json.loads(tokens[2])
    }
