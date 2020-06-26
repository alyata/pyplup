import websockets

class Showdown:
    def __init__(self, username = '', password = ''):
        self.uri = "ws://sim.smogon.com:8000/showdown/websocket"
        self.username = username
        self.password = password
        self.open = False

    async def run(self):
        async for messages in self.connection:
            await self.process_messages(messages)

    from ._showdown_process import process_messages

    # opens a connection
    async def connect(self):
        self.connection = await websockets.connect(self.uri)
        self.open = True

    # closes an existing connection
    async def close(self):
        if self.open:
            await self.connection.close()
            self.open = False
