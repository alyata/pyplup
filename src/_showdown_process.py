import json
from requests import post
import asyncio
from .parser import parse

"""
methods to process incoming messages and respond to them.
"""

async def process(self, message):
    params = parse(message)
    process_func = {
        "challstr": process_challstr,
    }.get(params["TYPE"], asyncio.coroutine(print))
    await process_func(self, params)

login_url = "http://play.pokemonshowdown.com/action.php"
async def process_challstr(self, params):
    post_body = {
        "act" : "login",
        "name" : self.username,
        "pass" : self.password,
        "challstr" : params["CHALLSTR"]
    }
    res = post(login_url, post_body)
    #ignore the leading '['
    response = json.loads(res.text[1:])
    if response["actionsuccess"]:
        await self.connection.send(f"/trn {self.username},0,{response['assertion']}")
        print(f"login succesful. USERNAME = {self.username}")
    else:
        print("login failed. Continuing as guest...")
