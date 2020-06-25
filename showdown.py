import websockets
import json
from requests import post
from parser import parse

class Showdown:
    def __init__(self, username = '', password = ''):
        self.uri = "ws://sim.smogon.com:8000/showdown/websocket"
        self.username = username
        self.password = password
        self.open = False

    async def run(self):
        async for messages in self.connection:
            for message in messages.split('\n'):
                await self.process(message)

    async def process(self, message):
        params = parse(message)
        if (params["TYPE"] == "challstr"):
            post_body = {
                "act" : "login",
                "name" : self.username,
                "pass" : self.password,
                "challstr" : params["CHALLSTR"]
            }
            res = post("http://play.pokemonshowdown.com/action.php", post_body)
            #ignore the leading '['
            response = json.loads(res.text[1:])
            print(response)
            if (response["actionsuccess"]):
                await self.connection.send(f"/trn {self.username},0,{response['assertion']}")
                print(f"login succesful. USERNAME = {self.username}")
            else:
                print("login failed. Continuing as guest...")
        else:
            print(params)

    # opens a connection
    async def connect(self):
        self.connection = await websockets.connect(self.uri)
        self.open = True

    # closes an existing connection
    async def close(self):
        if self.open:
            await self.connection.close()
            self.open = False
