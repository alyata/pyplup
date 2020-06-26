import websockets
from .constants import WEBSOCKET_URL

class Showdown:
    def __init__(self, username = '', password = ''):
        self.url = WEBSOCKET_URL
        self.username = username
        self.password = password
        self.open = False

    async def run(self):
        async for messages in self.connection:
            await self.process_messages(messages)

    from ._showdown_process import process_messages

    # opens a connection
    async def connect(self):
        self.connection = await websockets.connect(self.url)
        self.open = True

    # closes an existing connection
    async def close(self):
        if self.open:
            await self.connection.close()
            self.open = False
