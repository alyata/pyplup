import json
from .parser_gen import parse_def

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
        "init" : init,
        "title" : title,
        "users" : users,
        "join" : join,
        "j" : join,
        "J" : join,
        "leave" : leave,
        "l" : leave,
        "L" : leave,
        "battle" : battle,
        "b" : battle,
        "usercount" : usercount,
        "nametaken" : nametaken,
        "challstr" : challstr,
        "updateuser" : updateuser,
        "formats" : formats,
        "updatesearch" : updatesearch,
        "updatechallenges" : updatechallenges,
        "queryresponse" : queryresponse,
        "player" : player,
        "teamsize" : teamsize,
        "gametype" : gametype,
        "gen" : gen,
        "tier" : tier,
        "rated" : rated,
        "rule" : rule,
        "clearpoke" : clearpoke,
        "poke" : poke,
        "teampreview" : teampreview,
        "start" : start,
        "request" : request,
    }.get(type, parse_def)
    parsed = parse_func(tokens)
    parsed["ROOMID"] = roomid
    return parsed

"""
Room initialization
"""

#|init|ROOMTYPE
def init(tokens: [str]) -> dict:
    return {
        "TYPE" : "init",
        "ROOMTYPE" : tokens[1]
    }

#|title|TITLE
def title(tokens: [str]) -> dict:
    return {
        "TYPE" : "title",
        "TITLE" : tokens[1]
    }

#|users|USERLIST
def users(tokens: [str]) -> dict:
    return {
        "TYPE" : "users",
        "TITLE" : json.loads(tokens[1])
    }

"""
Room messages
"""
#|join|USER or |j|USER or |J|USER
def join(tokens: [str]) -> dict:
    return {
        "TYPE" : "join",
        "USER" : tokens[1]
    }

#|leave|USER or |l|USER or |L|USER
def leave(tokens: [str]) -> dict:
    return {
        "TYPE" : "leave",
        "USER" : tokens[1]
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
        "TYPE" : "usercount",
        "USERCOUNT" : int(tokens[1])
    }

#|nametaken|USERNAME|MESSAGE
def nametaken(tokens: [str]) -> dict:
    return {
        "TYPE" : "nametaken",
        "USERNAME" : tokens[1],
        "MESSAGE" : tokens[2]
    }

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

#|updateuser|USER|NAMED|AVATAR|SETTINGS
def updateuser(tokens: [str]) -> dict:
    return {
        "TYPE"     : "updateuser",
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
        "TYPE" : "formats",
        "FORMATSLIST" : format_sections
    }

#|updatesearch|JSON
def updatesearch(tokens: [str]) -> dict:
    return {
        "TYPE" : "updatesearch",
        "JSON" : json.loads(tokens[1])
    }

#|updatechallenges|JSON
def updatechallenges(tokens: [str]) -> dict:
    return {
        "TYPE" : "updatechallenges",
        "JSON" : json.loads(tokens[1])
    }

#|queryresponse|QUERYTYPE|JSON
def queryresponse(tokens: [str]) -> dict:
    return {
        "TYPE" : "queryresponse",
        "QUERYTYPE" : tokens[1],
        "JSON" : json.loads(tokens[2])
    }

"""
Pre-battle messages
"""

#|player|PLAYER|USERNAME|AVATAR|RATING
def player(tokens: [str]) -> dict:
    try:
        rating = tokens[4]
    except IndexError:
        rating = None
    return {
        "TYPE" : "player",
        "PLAYER" : tokens[1],
        "USERNAME" : tokens[2],
        "AVATAR" : tokens[3],
        "RATING" : rating
    }

#|teamsize|PLAYER|NUMBER
def teamsize(tokens: [str]) -> dict:
    return {
        "TYPE" : "teamsize",
        "PLAYER" : tokens[1],
        "NUMBER" : tokens[2]
    }

#|gametype|GAMETYPE
def gametype(tokens: [str]) -> dict:
    return {
        "TYPE" : "gametype",
        "GAMWTYPE" : tokens[1]
    }

#|gen|GENNUM
def gen(tokens: [str]) -> dict:
    return {
        "TYPE" : "gen",
        "GENNUM" : tokens[1]
    }

#|tier|FORMATNAME
def tier(tokens: [str]) -> dict:
    return {
        "TYPE" : "tier",
        "FORMATNAME" : tokens[1]
    }

#|rated|MESSAGE
def rated(tokens: [str]) -> dict:
    try:
        message = tokens[1]
    except IndexError:
        message = None
    return {
        "TYPE" : "rated",
        "MESSAGE" : message
    }

#|rule|RULE: DESCRIPTION
def rule(tokens: [str]) -> dict:
    rule, description = tokens[1].split(':', 1)
    return {
        "TYPE" : "rule",
        "RULE" : rule,
        "DESCRIPTION" : description
    }

#|clearpoke
def clearpoke(tokens: [str]) -> dict:
    return {
        "TYPE": "clearpoke"
    }

#|poke|PLAYER|DETAILS|ITEM
def poke(tokens: [str]) -> dict:
    details = parse_details(tokens[2])
    return {
        "TYPE" : "poke",
        "PLAYER" : tokens[1],
        "DETAILS" : details,
        "ITEM" : tokens[2] if tokens[2] else None
    }

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

#|teampreview
def teampreview(tokens: [str]) -> dict:
    return {
        "TYPE": "teampreview"
    }

#|start
def start(tokens: [str]) -> dict:
    return {
        "TYPE": "start"
    }

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
