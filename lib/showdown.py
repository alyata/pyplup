import websockets
import json
import asyncio
from requests import post
from .parser import parse

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

    from ._showdown_process import process_challstr

    async def process(self, message):
        params = parse(message)
        process_func = {
            "challstr": self.process_challstr,
        }.get(params["TYPE"], asyncio.coroutine(print))
        await process_func(params)

    # opens a connection
    async def connect(self):
        self.connection = await websockets.connect(self.uri)
        self.open = True

    # closes an existing connection
    async def close(self):
        if self.open:
            await self.connection.close()
            self.open = False
