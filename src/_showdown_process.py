import json
from requests import post
import asyncio
from .parser import parse
from .constants import LOGIN_URL

"""
methods to process incoming messages and respond to them.
"""

async def process_messages(self, messages):
    if messages[0] == '>':
        #non-global room message
        messages = messages[1:].split('\n')
        roomid = messages[0]
        messages = messages[1:]
    else:
        roomid = "global"
        messages = messages.split('\n')

    for message in messages:
        if message:
            await process(self, roomid, message)

async def process(self, roomid, message):
    params = parse(roomid, message)
    #by default, print the params to terminal
    default_func = asyncio.coroutine(lambda _,p: print(p))
    process_func = {
        "challstr": process_challstr,
        "updatechallenges": process_updatechallenges,
        "updateuser": process_updateuser,
        "request": process_request
    }.get(params["TYPE"], default_func)
    await process_func(self, params)

async def process_updateuser(self, params):
    print(f"login as USERNAME = {params['USER']} successful")

async def process_challstr(self, params):
    #send a POST request to verify credentials at showdown server
    post_body = {
        "act" : "login",
        "name" : self.username,
        "pass" : self.password,
        "challstr" : params["CHALLSTR"]
    }
    res = post(LOGIN_URL, post_body)
    #parse response as json
    response = json.loads(res.text[1:])
    #attempt login with verified credentials
    if response["actionsuccess"]:
        login_command = f"|/trn {self.username},0,{response['assertion']}"
        await self.connection.send(login_command)
    else:
        print("login failed. Aborting connection...")
        await self.close()

async def process_updatechallenges(self, params):
    # get a list of challengers
    challenges = params["JSON"]["challengesFrom"]
    # respond to exactly one challenge (if any)
    if challenges:
        challenger, format = challenges.popitem()
        if format == "gen8randombattle":
            print(f"accepting a random battle challenge from {challenger}")
            command = f"|/accept {challenger}"
        else:
            print(f"declining a challenge from {challenger}")
            command = f"|/reject {challenger}"
        await self.connection.send(command)

async def process_request(self, params):
    if params["REQUEST"]:
        battle_response = f"{params['ROOMID']}|/choose default"
        print(f"sending battle response: '{battle_response}'")
        await self.connection.send(battle_response)
